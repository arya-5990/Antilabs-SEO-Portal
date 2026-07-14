import asyncio
import sys
from bs4 import BeautifulSoup
import json

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from camoufox.async_api import AsyncCamoufox

async def main():
    url = "https://www.google.com/maps/place/The+Coffee+Concept+Rau/@22.6328865,75.8158135,3215m/data=!3m1!1e3!4m6!3m5!1s0x3962fb8573dd3873:0xc264111a708e01d6!8m2!3d22.6328904!4d75.8261085!16s%2Fg%2F11smm619r4?entry=tts&g_ep=EgoyMDI2MDYyMy4wIPu8ASoASAFQAw%3D%3D&skid=e3120883-339f-4013-bf37-a537ca37f82c"
    
    print("Launching Camoufox...")
    async with AsyncCamoufox(headless=True, geoip=True) as browser:
        page = await browser.new_page()
        await page.goto(url, wait_until="load", timeout=45000)
        await asyncio.sleep(7)
        html = await page.content()
        soup = BeautifulSoup(html, "lxml")
        
        ld_scripts = soup.find_all("script", type="application/ld+json")
        print("Number of application/ld+json scripts:", len(ld_scripts))
        for i, s in enumerate(ld_scripts):
            print(f"Script {i}:", s.string[:200] if s.string else "Empty")

        # Let's inspect meta description or other meta tags
        meta_desc = soup.find("meta", attrs={"name": "description"})
        print("Meta description:", meta_desc.get("content") if meta_desc else "None")

        og_desc = soup.find("meta", property="og:description")
        print("OG description:", og_desc.get("content") if og_desc else "None")

        # Let's check for class names/roles that contain phone, website etc.
        # Let's search for website link
        links = soup.find_all("a")
        web_links = [l.get("href") for l in links if l.get("href") and ("http" in l.get("href")) and ("google.com" not in l.get("href"))]
        print("Web links found on page:", web_links)

if __name__ == "__main__":
    asyncio.run(main())
