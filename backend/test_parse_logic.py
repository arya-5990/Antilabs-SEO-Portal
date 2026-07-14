import asyncio
import sys
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from camoufox.async_api import AsyncCamoufox

async def main():
    url = "https://www.google.com/maps/place/The+Coffee+Concept+Rau/@22.6328865,75.8158135,3215m/data=!3m1!1e3!4m6!3m5!1s0x3962fb8573dd3873:0xc264111a708e01d6!8m2!3d22.6328904!4d75.8261085!16s%2Fg%2F11smm619r4?entry=tts&g_ep=EgoyMDI2MDYyMy4wIPu8ASoASAFQAw%3D%3D&skid=e3120883-339f-4013-bf37-a537ca37f82c"
    
    print("Launching Camoufox...")
    async with AsyncCamoufox(headless=True, geoip=False) as browser:
        page = await browser.new_page(locale="en-US", extra_http_headers={"Accept-Language": "en-US,en;q=0.9"})
        await page.goto(url, wait_until="load", timeout=45000)
        await asyncio.sleep(6)
        
        title = await page.title()
        html = await page.content()
        soup = BeautifulSoup(html, "lxml")
        
        profile_data = {
            "url": url,
            "domain": urlparse(url).netloc,
            "business_name": "",
            "title": title,
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
            "scraper_tier": "camoufox",
        }
        
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
                
        # Regex matching rating & reviews
        rating_match = re.search(r'\b([1-5]\.\d)\b\s*\(([\d,]+)\)', text)
        if rating_match:
            profile_data["rating"] = rating_match.group(1)
            profile_data["review_count"] = rating_match.group(2).replace(",", "")
        else:
            rat_match = re.search(r'\b([1-5]\.\d)\b', text)
            if rat_match:
                profile_data["rating"] = rat_match.group(1)
                
        cat_match = re.search(r'([1-5]\.\d)\s*\([\d,]+\)\s*(?:·\s*[^·]+)?·\s*([^·\n]{2,30})', text)
        if cat_match:
            category_candidate = cat_match.group(2).strip()
            if category_candidate and not any(bad in category_candidate.lower() for bad in ["overview", "menu", "reviews", "about", "directions"]):
                profile_data["categories"] = category_candidate
                
        address_match = re.search(r'([^·\n]{15,100}?\b\d{5,6}\b)', text)
        if address_match:
            profile_data["address"] = address_match.group(1).strip()
            
        print("\nExtracted profile_data:")
        for k, v in profile_data.items():
            if k == "text":
                print(f"  {k}: {str(v)[:200]}...")
            else:
                print(f"  {k}: {v}")

if __name__ == "__main__":
    asyncio.run(main())
