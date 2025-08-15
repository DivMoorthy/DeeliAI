from playwright.sync_api import sync_playwright
import re
import time

class Yahoo:
    def get_eps(ticker):
        url = "https://finance.yahoo.com/quote/" + ticker + "/"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url, timeout=60000)

            # Wait until page fully loads
            page.wait_for_load_state("networkidle")


            # Get all visible text on the page
            full_text = page.inner_text("body")

            # Search specifically for "EPS (TTM)" followed by a number
            match = re.search(r"EPS\s*\(TTM\)\s*([\-\d.,]+)", full_text)

            browser.close()

            return match.group(1) if match else None

    if __name__ == "__main__":
        eps_value = get_eps()
        if eps_value:
            print(f"EPS (TTM): {eps_value}")
        else:
            print("EPS (TTM) not found.")