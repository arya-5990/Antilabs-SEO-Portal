import asyncio
import httpx
import re
import os
import json
import hashlib
from urllib.parse import urlparse, unquote
from cachetools import TTLCache
from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
import models
from services.gbp_analyzer import analyze_gbp
from dependencies import limiter

router = APIRouter()

# Cache up to 50 GBP reports for 24 hours (86400 seconds)
gbp_cache = TTLCache(maxsize=50, ttl=86400)


def get_gbp_cache_key(profile_url: str) -> str:
    return hashlib.md5(profile_url.encode()).hexdigest()


class GBPReportRequest(BaseModel):
    profile_url: str  # Google Business Profile URL or Google Maps URL


async def _resolve_short_url(url: str) -> str:
    """Resolve shortened Google Maps URLs (maps.app.goo.gl) to full URLs."""
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
            resp = await client.head(url)
            final_url = str(resp.url)
            print(f"[GBP] Resolved short URL -> {final_url}")
            return final_url
    except Exception as e:
        print(f"[GBP] Failed to resolve short URL: {e}")
        return url


def _extract_business_name_from_url(url: str) -> str:
    """Extract business name from Google Maps URL path."""
    try:
        # URLs like: google.com/maps/place/Business+Name+Here/...
        match = re.search(r'/maps/place/([^/@]+)', url)
        if match:
            name = unquote(match.group(1)).replace('+', ' ')
            # Clean up any trailing data references
            name = re.sub(r'/data.*$', '', name)
            return name.strip()
    except Exception:
        pass
    return ""


async def _scrape_google_maps_page(url: str) -> dict:
    """
    Specialized scraper for Google Maps pages.
    First, attempts dynamic JavaScript scraping using AsyncCamoufox.
    Falls back to a lightweight meta-tag scraper using httpx if Camoufox fails.
    """
    profile_data = {
        "url": url,
        "domain": urlparse(url).netloc,
        "business_name": "",
        "title": "",
        "meta_description": "",
        "og_image": "",
        "address": "",
        "rating": "",
        "review_count": "",
        "phone": "",
        "website": "",
        "categories": "",
        "hours": "",
        "h1": [],
        "h2": [],
        "h3": [],
        "text": "",
        "scraper_tier": "google-maps-meta",
    }

    try:
        from camoufox.async_api import AsyncCamoufox
        from bs4 import BeautifulSoup

        print(f"[GBP-Scraper] Attempting dynamic Camoufox scrape for: {url}")
        async with AsyncCamoufox(headless=True, geoip=False) as browser:
            page = await browser.new_page(locale="en-US", extra_http_headers={"Accept-Language": "en-US,en;q=0.9"})
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(6)  # Allow dynamic components to render
            
            title = await page.title()
            profile_data["title"] = title
            
            html = await page.content()
            soup = BeautifulSoup(html, "lxml")
            
            h1s = [h.get_text(strip=True) for h in soup.find_all("h1") if h.get_text(strip=True)]
            profile_data["h1"] = h1s
            if h1s:
                profile_data["business_name"] = h1s[0]
            else:
                profile_data["business_name"] = re.sub(r'\s*[-–]\s*Google\s*Maps?\s*$', '', title, flags=re.I).strip()
            
            for tag in soup(["script", "style", "noscript", "iframe"]):
                tag.decompose()
            text = soup.get_text(separator=" ", strip=True)
            text = re.sub(r"\s+", " ", text)[:8000]
            text = text.encode("utf-8", errors="ignore").decode("utf-8")
            profile_data["text"] = text
            
            # Extract website link
            links = soup.find_all("a")
            web_links = []
            for l in links:
                href = l.get("href")
                if href and "http" in href:
                    href_lower = href.lower()
                    if not any(domain in href_lower for domain in ["google.com", "google.co.", "gstatic.com", "ggpht.com", "youtube.com", "twitter.com", "facebook.com", "instagram.com"]):
                        web_links.append(href)
            if web_links:
                direct_links = [wl for wl in web_links if not any(food in wl.lower() for food in ["swiggy", "zomato", "uber", "grubhub", "doordash", "dineout"])]
                if direct_links:
                    profile_data["website"] = direct_links[0]
                else:
                    profile_data["website"] = web_links[0]
            
            # Extract rating and review count from text
            rating_match = re.search(r'\b([1-5]\.\d)\b\s*\(([\d,]+)\)', text)
            if rating_match:
                profile_data["rating"] = rating_match.group(1)
                profile_data["review_count"] = rating_match.group(2).replace(",", "")
            else:
                rat_match = re.search(r'\b([1-5]\.\d)\b', text)
                if rat_match:
                    profile_data["rating"] = rat_match.group(1)
            
            # Extract category
            category_candidate = ""
            cat_match = re.search(r'([1-5]\.\d)\s*\([\d,]+\)\s*(?:·\s*[^·]+)?·\s*([^·\n]{2,30})', text)
            if cat_match:
                category_candidate = cat_match.group(2).strip()
                if any(x in category_candidate for x in ["Dine-in", "Takeout", "Delivery"]):
                    parts = text.split("·")
                    for p in parts:
                        p_clean = p.strip()
                        p_clean = re.sub(r'[^\w\s-]', '', p_clean).strip()
                        p_clean = re.sub(r'\b(Overview|Menu|Reviews|About|Directions|Save|Nearby|Share)\b', '', p_clean, flags=re.I).strip()
                        if p_clean and not any(x in p_clean for x in ["Dine-in", "Takeout", "Delivery"]):
                            if not any(c in p_clean for c in ["₹", "$"]) and not re.search(r'\d', p_clean):
                                words = p_clean.split()
                                if len(words) <= 3 and len(p_clean) < 30:
                                    category_candidate = p_clean
                                    break
            profile_data["categories"] = category_candidate
            
            # Extract address (with ZIP code / PIN code format)
            address_match = re.search(r'([^·\n]{15,100}?\b\d{5,6}\b)', text)
            if address_match:
                addr = address_match.group(1).strip()
                # Filter out PUA characters (often used as icons)
                addr = "".join(c for c in addr if not (0xE000 <= ord(c) <= 0xF8FF))
                # Clean up punctuation & leading metadata
                addr = re.sub(r'[^\w\s,.-]', '', addr)
                addr = addr.strip()
                prev_addr = None
                while addr != prev_addr:
                    prev_addr = addr
                    addr = re.sub(r'^\s*(No-contact delivery|Dine-in|Takeout|Delivery|Open|Closed|Order online|Reserve a table|a table|Order food|Drive-through|Service options|Identify as women-led|Health  safety|Highlights|Accessibility|Offerings|Dining options|Amenities|Atmosphere|Crowd|Planning|Payments)\b\s*', '', addr, flags=re.I)
                    addr = re.sub(r'^[^\w\s]*', '', addr).strip()
                profile_data["address"] = addr
                
            profile_data["scraper_tier"] = "camoufox"
            print(f"[GBP-Scraper] Camoufox SUCCESS: name='{profile_data['business_name']}', "
                  f"rating='{profile_data['rating']}', reviews='{profile_data['review_count']}', "
                  f"website='{profile_data['website']}', address='{profile_data['address']}', "
                  f"categories='{profile_data['categories']}'")
            return profile_data

    except Exception as cam_err:
        print(f"[GBP-Scraper] Camoufox scraper failed: {cam_err}. Falling back to old static scraping.")

    # FALLBACK to original static HTTPX-based scraper
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
        }
        async with httpx.AsyncClient(follow_redirects=True, timeout=25) as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            html = resp.text

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "lxml")

        # --- Extract from <meta> tags (available even without JS) ---
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
            profile_data["title"] = title
            biz_name = re.sub(r'\s*[-–]\s*Google\s*Maps?\s*$', '', title, flags=re.I).strip()
            if biz_name:
                profile_data["business_name"] = biz_name

        meta_desc_tag = soup.find("meta", attrs={"name": re.compile(r"description", re.I)})
        if meta_desc_tag:
            profile_data["meta_description"] = meta_desc_tag.get("content", "").strip()

        for og in soup.find_all("meta", property=re.compile(r"^og:", re.I)):
            prop = og.get("property", "").lower()
            content = og.get("content", "")
            if prop == "og:title":
                profile_data["title"] = profile_data["title"] or content
                if not profile_data["business_name"]:
                    profile_data["business_name"] = re.sub(r'\s*[-–]\s*Google\s*Maps?\s*$', '', content, flags=re.I).strip()
            elif prop == "og:description":
                profile_data["meta_description"] = profile_data["meta_description"] or content
            elif prop == "og:image":
                profile_data["og_image"] = content

        for script in soup.find_all("script", type="application/ld+json"):
            try:
                ld_data = json.loads(script.string)
                if isinstance(ld_data, dict):
                    if ld_data.get("@type") in ("LocalBusiness", "Restaurant", "Store", "Organization", "Place"):
                        profile_data["business_name"] = profile_data["business_name"] or ld_data.get("name", "")
                        if "address" in ld_data:
                            addr = ld_data["address"]
                            if isinstance(addr, dict):
                                profile_data["address"] = f"{addr.get('streetAddress', '')}, {addr.get('addressLocality', '')}, {addr.get('addressRegion', '')} {addr.get('postalCode', '')}".strip(", ")
                            elif isinstance(addr, str):
                                profile_data["address"] = addr
                        if "aggregateRating" in ld_data:
                            rating = ld_data["aggregateRating"]
                            profile_data["rating"] = str(rating.get("ratingValue", ""))
                            profile_data["review_count"] = str(rating.get("reviewCount", ""))
                        profile_data["phone"] = ld_data.get("telephone", "")
                        if "url" in ld_data:
                            profile_data["website"] = ld_data["url"]
            except (json.JSONDecodeError, TypeError):
                continue

        all_scripts = soup.find_all("script")
        script_text = " ".join(s.string or "" for s in all_scripts)

        rating_match = re.search(r'"(\d\.\d)"\s*,\s*"(\d+)\s*reviews?"', script_text, re.I)
        if rating_match and not profile_data["rating"]:
            profile_data["rating"] = rating_match.group(1)
            profile_data["review_count"] = rating_match.group(2)

        desc = profile_data["meta_description"]
        if desc and not profile_data["address"]:
            parts = desc.split("·")
            if len(parts) >= 3:
                profile_data["address"] = parts[-1].strip()
            elif len(parts) == 2:
                profile_data["address"] = parts[-1].strip()

        if desc and not profile_data["rating"]:
            rating_in_desc = re.search(r'(\d+\.?\d*)\s*(?:stars?|★)', desc, re.I)
            if rating_in_desc:
                profile_data["rating"] = rating_in_desc.group(1)
            review_in_desc = re.search(r'(\d+[\d,]*)\s*reviews?', desc, re.I)
            if review_in_desc:
                profile_data["review_count"] = review_in_desc.group(1).replace(",", "")

        if desc:
            category_match = re.search(r'·\s*([^·★]+?)\s*·', desc)
            if category_match:
                profile_data["categories"] = category_match.group(1).strip()

        if not profile_data["business_name"]:
            profile_data["business_name"] = _extract_business_name_from_url(url)

        for tag in soup(["script", "style", "noscript", "iframe"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        text = re.sub(r"\s+", " ", text)[:6000]
        text = text.encode("utf-8", errors="ignore").decode("utf-8")
        profile_data["text"] = text

        print(f"[GBP-Scraper] Static Extracted: name='{profile_data['business_name']}', "
              f"rating={profile_data['rating']}, reviews={profile_data['review_count']}, "
              f"address='{profile_data['address']}', categories='{profile_data['categories']}'")

    except Exception as e:
        print(f"[GBP-Scraper] Static scraper exception: {e}")
        profile_data["scraper_tier"] = "failed"

    return profile_data


@router.post("/gbp-report")
@limiter.limit("5/minute")
async def generate_gbp_report(request: Request, body: GBPReportRequest, db: Session = Depends(get_db)):
    try:
        profile_url = body.profile_url.strip().rstrip("/")

        if not profile_url:
            raise HTTPException(status_code=400, detail="Profile URL is required")

        # Resolve short URLs (maps.app.goo.gl, share.google) to full Google Maps URLs
        if "goo.gl" in profile_url or "maps.app" in profile_url or "share.google" in profile_url:
            profile_url = await _resolve_short_url(profile_url)

        # If it resolves to a google search URL, convert it to a maps search query
        if "google.com/search" in profile_url:
            from urllib.parse import parse_qs, quote_plus
            parsed_url = urlparse(profile_url)
            params = parse_qs(parsed_url.query)
            q_param = params.get("q")
            if q_param:
                query = q_param[0]
                profile_url = f"https://www.google.com/maps/search/?api=1&query={quote_plus(query)}"
                print(f"[GBP] Converted Google Search URL to Maps Search: {profile_url}")

        cache_key = get_gbp_cache_key(profile_url)
        # Cache check bypassed to ensure real/fresh data is fetched every time
        # if cache_key in gbp_cache:
        #     print(f"[gbp-report] Returning cached result for {profile_url}")
        #     return gbp_cache[cache_key]

        # Use specialized Google Maps scraper
        print(f"[gbp-report] Scraping Google Maps page: {profile_url}")
        profile_data = await _scrape_google_maps_page(profile_url)

        # If business name is still empty, try to extract from URL
        if not profile_data.get("business_name"):
            profile_data["business_name"] = _extract_business_name_from_url(profile_url)

        # Run GBP-specific AI analysis
        report = analyze_gbp(profile_data)

        # Attach scraper tier info for debugging
        report["_scraper_info"] = {
            "tier": profile_data.get("scraper_tier"),
            "scraped_name": profile_data.get("business_name", ""),
            "scraped_rating": profile_data.get("rating", ""),
        }

        # Save to database (memory cache disabled to ensure real data is fetched)
        if "error" not in report:
            # Save to DB
            db_report = models.GBPReport(
                profile_url=profile_url,
                business_name=report.get("business_name", profile_data.get("business_name", "Unknown")),
                overall_score=report.get("overall_score", 0),
                report_data=report
            )
            db.add(db_report)
            db.commit()

        return report

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gbp-history")
async def get_gbp_history(limit: int = 10, db: Session = Depends(get_db)):
    reports = db.query(models.GBPReport).order_by(models.GBPReport.created_at.desc()).limit(limit).all()
    return [
        {
            "id": r.id,
            "profile_url": r.profile_url,
            "business_name": r.business_name,
            "overall_score": r.overall_score,
            "created_at": r.created_at
        }
        for r in reports
    ]


@router.get("/gbp-history/{report_id}")
async def get_gbp_report_by_id(report_id: int, db: Session = Depends(get_db)):
    report = db.query(models.GBPReport).filter(models.GBPReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="GBP report not found")
    return report.report_data
