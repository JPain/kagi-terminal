"""Render mock.html (a hand-made page using Kagi class names, not a real Kagi page) to mock.png."""
import asyncio, pathlib
from playwright.async_api import async_playwright
here = pathlib.Path(__file__).parent
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        p = await b.new_page(viewport={'width': 960, 'height': 680}, device_scale_factor=2)
        await p.goto((here / 'mock.html').as_uri())
        await p.screenshot(path=str(here / 'mock.png'))
        await b.close()
asyncio.run(main())
