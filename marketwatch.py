from playwright.sync_api import sync_playwright
import re

def get_rd_expense(ticker: str) -> str:
    """

    **RD alternate source scraper**
    Scrapes MarketWatch financials for a company's R&D expense.
    Returns the latest R&D amount or a message if not found.
    """
    ticker = ticker.upper()
    url = f"https://www.marketwatch.com/investing/stock/{ticker}/financials"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_load_state("networkidle")

        # Scroll to ensure all content is loaded
        for _ in range(3):
            page.mouse.wheel(0, 800)
            page.wait_for_timeout(500)

        # Grab page text
        body_text = page.inner_text("body")
        browser.close()

    # Search for "Research & Development" or "R&D" followed by a number
    match = re.search(r"(Research & Development|R&D)[^\d$]*\$?([\d,]+)", body_text, re.IGNORECASE)
    if match:
        rd_value = match.group(2)
        return f"Latest R&D expense for {ticker}: ${rd_value}"
    else:
        return f"R&D expense not found for {ticker}."

