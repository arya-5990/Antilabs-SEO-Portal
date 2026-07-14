import asyncio
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# ─────────────────────────────────────────────
# TIER 1 — Crawl4AI  (fast async stealth scraper)
# ─────────────────────────────────────────────
async def _scrape_with_crawl4ai(url: str) -> dict | None:
    """
    First attempt: Crawl4AI with stealth mode.
    Handles JS-rendered pages, removes navigator.webdriver flag.
    Returns None if blocked or content is too thin.
    """
    try:
        from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

        browser_cfg = BrowserConfig(
            enable_stealth=True,
            headless=True,
        )
        run_cfg = CrawlerRunConfig(
            word_count_threshold=10,
            remove_overlay_elements=True,
            magic=True,            # auto-dismiss popups / cookie banners
        )

        async with AsyncWebCrawler(config=browser_cfg) as crawler:
            result = await crawler.arun(url=url, config=run_cfg)

        if not result.success or not result.cleaned_html:
            print(f"[Crawl4AI] Failed or empty for {url}: {result.error_message}")
            return None

        return _parse_html(result.cleaned_html, url)

    except Exception as e:
        print(f"[Crawl4AI] Exception for {url}: {e}")
        return None


# ─────────────────────────────────────────────
# TIER 2 — Camoufox  (Firefox anti-detect browser)
# ─────────────────────────────────────────────
async def _scrape_with_camoufox(url: str) -> dict | None:
    """
    Fallback: Camoufox — a patched Firefox with engine-level fingerprint spoofing.
    Generates a unique, statistically-valid browser profile every session
    (WebGL, canvas, fonts, WebRTC, screen size, timezone, locale…).
    Much harder to detect than Playwright or standard Chromium.
    """
    try:
        from camoufox.async_api import AsyncCamoufox

        async with AsyncCamoufox(headless=True, geoip=True) as browser:
            page = await browser.new_page()

            # Human-like: random small delay before goto
            await asyncio.sleep(0.5)
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)

            # Wait for body to be populated
            await page.wait_for_selector("body", timeout=10000)
            html = await page.content()

        if not html:
            print(f"[Camoufox] Empty content for {url}")
            return None

        return _parse_html(html, url)

    except Exception as e:
        print(f"[Camoufox] Exception for {url}: {e}")
        return None


# ─────────────────────────────────────────────
# HTML Parser — shared by both tiers
# ─────────────────────────────────────────────
def _parse_html(html: str, url: str) -> dict:
    """Parse raw HTML and extract SEO-relevant fields."""
    soup = BeautifulSoup(html, "lxml")

    # Remove noise
    for tag in soup(["script", "style", "nav", "footer", "noscript", "iframe"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title and soup.title.string else ""

    meta_desc = ""
    meta_tag = soup.find("meta", attrs={"name": re.compile(r"description", re.I)})
    if meta_tag:
        meta_desc = meta_tag.get("content", "").strip()

    h1s = [h.get_text(strip=True) for h in soup.find_all("h1") if h.get_text(strip=True)]
    h2s = [h.get_text(strip=True) for h in soup.find_all("h2") if h.get_text(strip=True)]
    h3s = [h.get_text(strip=True) for h in soup.find_all("h3") if h.get_text(strip=True)]

    # Grab OG tags for richer data
    og_title = ""
    og_desc  = ""
    og_image = ""
    for og in soup.find_all("meta", property=re.compile(r"^og:", re.I)):
        prop = og.get("property", "").lower()
        content = og.get("content", "")
        if prop == "og:title":
            og_title = content
        elif prop == "og:description":
            og_desc = content
        elif prop == "og:image":
            og_image = content

    # Body text — limit to avoid token overflow
    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text)[:6000]
    # Sanitize: remove non-encodable chars to prevent Windows charmap errors
    text = text.encode("utf-8", errors="ignore").decode("utf-8")

    parsed = urlparse(url)

    return {
        "url": url,
        "domain": parsed.netloc,
        "title": title or og_title,
        "meta_description": meta_desc or og_desc,
        "og_image": og_image,
        "h1": h1s,
        "h2": h2s,
        "h3": h3s,
        "text": text,
    }


# ─────────────────────────────────────────────
# Public API — 2-tier entry point
# ─────────────────────────────────────────────
async def scrape_website(url: str) -> dict:
    """
    2-tier anti-bot scraper:
      Tier 1: Crawl4AI  (fast, async, stealth)
      Tier 2: Camoufox  (Firefox anti-detect, engine-level fingerprint spoofing)

    Falls back to Tier 2 automatically if Tier 1 is blocked or returns thin content.
    """
    print(f"[Scraper] Tier 1 (Crawl4AI) -> {url}")
    result = await _scrape_with_crawl4ai(url)

    # Consider content "thin" if less than 200 chars of body text
    if result and len(result.get("text", "")) > 200:
        print(f"[Scraper] Tier 1 SUCCESS for {url}")
        result["scraper_tier"] = "crawl4ai"
        return result

    print(f"[Scraper] Tier 1 thin/blocked -- switching to Tier 2 (Camoufox) -> {url}")
    result = await _scrape_with_camoufox(url)

    if result:
        print(f"[Scraper] Tier 2 SUCCESS for {url}")
        result["scraper_tier"] = "camoufox"
        return result

    # Both tiers failed
    print(f"[Scraper] Both tiers failed for {url}")
    return {
        "url": url,
        "domain": urlparse(url).netloc,
        "error": "Both Crawl4AI and Camoufox failed to scrape this URL. "
                 "The site may require a CAPTCHA solve or residential proxies.",
        "scraper_tier": "failed",
    }
