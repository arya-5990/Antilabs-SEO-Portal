import asyncio
import httpx
import re
import os
from urllib.parse import urlparse
import hashlib
from cachetools import TTLCache
from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from database import get_db
import models
from services.scraper import scrape_website
from services.ai_analyzer import analyze_competitors
from dependencies import limiter

router = APIRouter()

# Cache up to 100 analysis results for 24 hours (86400 seconds)
analysis_cache = TTLCache(maxsize=100, ttl=86400)

def get_cache_key(our_url: str, competitor_url: str) -> str:
    key_str = f"{our_url}|{competitor_url}"
    return hashlib.md5(key_str.encode()).hexdigest()

class AnalyzeRequest(BaseModel):
    our_url: HttpUrl
    competitor_url: HttpUrl
    captcha_token: str | None = None

async def verify_captcha(token: str | None):
    secret_key = os.getenv("RECAPTCHA_SECRET_KEY")
    # If key is not configured, bypass verification for local testing
    if not secret_key or secret_key == "your_recaptcha_secret_here":
        return True

    if not token:
        raise HTTPException(status_code=400, detail="CAPTCHA token is missing")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": secret_key, "response": token},
        )
        result = response.json()
        if not result.get("success"):
            raise HTTPException(status_code=400, detail="Invalid CAPTCHA")
    return True


async def _simple_httpx_scrape(url: str) -> dict | None:
    """
    Lightweight fallback scraper using plain httpx (no browser needed).
    Works for static / SSR pages. Returns None on failure.
    """
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }
        async with httpx.AsyncClient(follow_redirects=True, timeout=20) as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            html = resp.text

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "lxml")

        for tag in soup(["script", "style", "nav", "footer", "noscript", "iframe"]):
            tag.decompose()

        title = soup.title.string.strip() if soup.title and soup.title.string else ""
        meta_tag = soup.find("meta", attrs={"name": re.compile(r"description", re.I)})
        meta_desc = meta_tag.get("content", "").strip() if meta_tag else ""
        h1s = [h.get_text(strip=True) for h in soup.find_all("h1") if h.get_text(strip=True)]
        h2s = [h.get_text(strip=True) for h in soup.find_all("h2") if h.get_text(strip=True)]
        h3s = [h.get_text(strip=True) for h in soup.find_all("h3") if h.get_text(strip=True)]
        text = soup.get_text(separator=" ", strip=True)
        text = re.sub(r"\s+", " ", text)[:6000]
        text = text.encode("utf-8", errors="ignore").decode("utf-8")
        parsed = urlparse(url)

        if len(text) < 100:
            return None

        return {
            "url": url,
            "domain": parsed.netloc,
            "title": title,
            "meta_description": meta_desc,
            "og_image": "",
            "h1": h1s,
            "h2": h2s,
            "h3": h3s,
            "text": text,
            "scraper_tier": "httpx-fallback",
        }
    except Exception as e:
        print(f"[httpx-fallback] Failed for {url}: {e}")
        return None


def _minimal_data(url: str) -> dict:
    """Returns bare-minimum dict when all scraping fails."""
    parsed = urlparse(url)
    return {
        "url": url,
        "domain": parsed.netloc,
        "title": "",
        "meta_description": "",
        "og_image": "",
        "h1": [],
        "h2": [],
        "h3": [],
        "text": f"Website at {parsed.netloc}",
        "scraper_tier": "none",
    }


@router.post("/analyze")
@limiter.limit("5/minute")
async def analyze(request: Request, body: AnalyzeRequest, db: Session = Depends(get_db)):
    try:
        await verify_captcha(body.captcha_token)

        our_url_str = str(body.our_url).rstrip("/")
        competitor_url_str = str(body.competitor_url).rstrip("/")

        cache_key = get_cache_key(our_url_str, competitor_url_str)
        if cache_key in analysis_cache:
            print(f"[analyze] Returning cached result for {our_url_str} vs {competitor_url_str}")
            return analysis_cache[cache_key]

        # Tier 1+2: Crawl4AI / Camoufox
        our_data, competitor_data = await asyncio.gather(
            scrape_website(our_url_str),
            scrape_website(competitor_url_str),
        )

        # Tier 3: plain httpx fallback when heavy scrapers fail
        if our_data.get("scraper_tier") == "failed":
            print(f"[analyze] Tier 3 httpx fallback for our URL: {our_url_str}")
            our_data = await _simple_httpx_scrape(our_url_str) or _minimal_data(our_url_str)

        if competitor_data.get("scraper_tier") == "failed":
            print(f"[analyze] Tier 3 httpx fallback for competitor URL: {competitor_url_str}")
            competitor_data = await _simple_httpx_scrape(competitor_url_str) or _minimal_data(competitor_url_str)

        # Run AI analysis
        analysis_result = analyze_competitors(our_data, competitor_data)

        # Attach scraper tier info for debugging / transparency
        analysis_result["_scraper_info"] = {
            "our_tier": our_data.get("scraper_tier"),
            "competitor_tier": competitor_data.get("scraper_tier"),
        }

        # Save to cache and database
        if "error" not in analysis_result:
            analysis_cache[cache_key] = analysis_result
            
            # Save to DB
            db_report = models.AnalysisReport(
                our_url=our_url_str,
                competitor_url=competitor_url_str,
                our_score=analysis_result.get("our_score", 0),
                competitor_score=analysis_result.get("competitor_score", 0),
                report_data=analysis_result
            )
            db.add(db_report)
            db.commit()

        return analysis_result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_history(limit: int = 10, db: Session = Depends(get_db)):
    reports = db.query(models.AnalysisReport).order_by(models.AnalysisReport.created_at.desc()).limit(limit).all()
    return [{"id": r.id, "our_url": r.our_url, "competitor_url": r.competitor_url, "our_score": r.our_score, "competitor_score": r.competitor_score, "created_at": r.created_at} for r in reports]

@router.get("/history/{report_id}")
async def get_report_by_id(report_id: int, db: Session = Depends(get_db)):
    report = db.query(models.AnalysisReport).filter(models.AnalysisReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Analysis report not found")
    return report.report_data

