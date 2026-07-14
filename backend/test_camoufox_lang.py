import asyncio
import sys

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from camoufox.async_api import AsyncCamoufox

async def main():
    url = "https://www.google.com/maps/place/The+Coffee+Concept+Rau/@22.6328865,75.8158135,3215m/data=!3m1!1e3!4m6!3m5!1s0x3962fb8573dd3873:0xc264111a708e01d6!8m2!3d22.6328904!4d75.8261085!16s%2Fg%2F11smm619r4?entry=tts&g_ep=EgoyMDI2MDYyMy4wIPu8ASoASAFQAw%3D%3D&skid=e3120883-339f-4013-bf37-a537ca37f82c"
    
    print("Launching Camoufox with en-US locale...")
    # Playwright accepts locale in context options or launch options.
    # In Camoufox, we can pass locale to AsyncCamoufox or new_page. Let's try both or new_page(locale="en-US").
    async with AsyncCamoufox(headless=True, geoip=False) as browser:
        # geoip=False will prevent it from changing timezone/locale based on IP.
        # Let's see if we can set locale to en-US.
        page = await browser.new_page(locale="en-US", extra_http_headers={"Accept-Language": "en-US,en;q=0.9"})
        await page.goto(url, wait_until="load", timeout=45000)
        await asyncio.sleep(5)
        title = await page.title()
        print("Page Title:", title)
        
        # Print a snippet of body text to check language
        from bs4 import BeautifulSoup
        html = await page.content()
        soup = BeautifulSoup(html, "lxml")
        text = soup.get_text(separator=" ", strip=True)
        print("Text snippet (first 500 chars):", text[:500])

if __name__ == "__main__":
    asyncio.run(main())
