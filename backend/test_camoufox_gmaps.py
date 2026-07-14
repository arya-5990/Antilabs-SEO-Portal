import asyncio
import sys
from bs4 import BeautifulSoup

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
        print("Navigating to URL...")
        await page.goto(url, wait_until="load", timeout=45000)
        
        print("Waiting 7 seconds for dynamic content...")
        await asyncio.sleep(7)
        
        # Print page title
        title = await page.title()
        print("Page Title:", title)
        
        html = await page.content()
        soup = BeautifulSoup(html, "lxml")
        
        # Find H1
        h1s = [h.get_text(strip=True) for h in soup.find_all("h1")]
        print("H1 elements:", h1s)
        
        # Let's search for "Coffee" or other text in the page
        print("Is 'Coffee' in HTML?", "Coffee" in html or "coffee" in html.lower())
        
        # Print a snippet of body text
        text = soup.get_text(separator=" ", strip=True)
        print("Text snippet (length {}):".format(len(text)), text[:1000])

if __name__ == "__main__":
    asyncio.run(main())
