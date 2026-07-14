import asyncio
import sys

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from api.gbp_report import _resolve_short_url, _scrape_google_maps_page

async def main():
    url = "https://maps.app.goo.gl/7FMF3a6XBzVRMbxh6"
    print("Resolving short URL...")
    resolved = await _resolve_short_url(url)
    print("Resolved URL:", resolved)
    
    print("\nScraping resolved URL...")
    data = await _scrape_google_maps_page(resolved)
    print("\nScraped Data:")
    for k, v in data.items():
        if k == "text":
            print(f"  {k}: {str(v)[:200]}...")
        else:
            print(f"  {k}: {v}")

if __name__ == "__main__":
    asyncio.run(main())
