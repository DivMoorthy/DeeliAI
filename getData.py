from playwright.sync_api import sync_playwright
import os
import re

class Data:
    def search_edgar_10k_viewer(url: str, keyword: str) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                # Navigate to the 10-K viewer page
                page.goto(url, timeout=60000)

                # Wait for search input to be ready (in viewer top bar)
                page.wait_for_selector('#searchbox', timeout=10000)

                # Type the keyword and press Enter
                page.fill('#searchbox', keyword)
                page.keyboard.press('Enter')

                # Wait for search results to load
                page.wait_for_selector('.searchhit', timeout=10000)

                # Extract and return the first match
                result = page.locator('.searchhit').first.inner_text()
                return result

            except Exception as e:
                return f"❌ Error during search: {e}"
            finally:
                browser.close()
