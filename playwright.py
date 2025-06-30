import asyncio
from playwright.async_api import async_playwright

async def scrape_quotes():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://quotes.toscrape.com")

        # Select the first quote and author
        quote = await page.text_content(".quote:nth-child(1) .text")
        author = await page.text_content(".quote:nth-child(1) .author")

        print(f"Quote: {quote}")
        print(f"Author: {author}")

        await browser.close()

# Run the async function
asyncio.run(scrape_quotes())