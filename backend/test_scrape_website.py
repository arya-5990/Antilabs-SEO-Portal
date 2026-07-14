import asyncio
import sys

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from services.scraper import scrape_website
from api.gbp_report import _resolve_short_url

async def main():
    url = "https://www.google.com/maps/place/ROYAL+VET+CLINIC/@22.7183628,75.8405459,270m/data=!3m1!1e3!4m6!3m5!1s0x3962fd115d041cd9:0xcef1a7a87439d9de!8m2!3d22.7186253!4d75.8409981!16s%2Fg%2F11xmnwcb8c?entry=tts&g_ep=EgoyMDI2MDYyMy4wIPu8ASoASAFQAw%3D%3D&skid=6a900b0d-2ea5-4056-bafa-bbc0bb52ec7f"
    print("Resolving short URL...")
    resolved = await _resolve_short_url(url)
    print("Resolved URL:", resolved)
    
    print("\nScraping with scrape_website (Crawl4AI / Camoufox)...")
    result = await scrape_website(resolved)
    print("\nResult:")
    for k, v in result.items():
        if k == "text":
            print(f"  {k}: {str(v)[:200]}...")
        else:
            print(f"  {k}: {v}")

if __name__ == "__main__":
    asyncio.run(main())
