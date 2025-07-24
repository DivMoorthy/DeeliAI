from playwright.sync_api import sync_playwright
import os
import re


class Data:
    @staticmethod
    def search_edgar_10k_viewer(url: str, keyword: str) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=100)  # slow_mo for visibility
            page = browser.new_page()

            try:
                print("🔍 Navigating to page...")
                page.goto(url, timeout=60000)
                page.wait_for_load_state("networkidle")

                # Wait for the input box to be visible
                search_input = page.locator('input#global-search')
                search_input.wait_for(timeout=15000)
                print("✅ Found search box")

                # Click, type the keyword, and press Enter
                search_input.click()
                search_input.fill(keyword)
                search_input.press('Enter')

                print(f"⌨️ Typed keyword: {keyword}")

                # Wait for highlights or search results to appear
                # In the iXBRL viewer, search results often trigger fact highlights
                # We'll wait a bit or look for something like .searchhit or a highlight
                time.sleep(5)  # Let the highlights render

                # Optional: capture a screenshot to verify
                page.screenshot(path="search_result.png")
                print("📸 Screenshot saved")

                # Keep browser open for manual inspection if needed
                print("⏳ Done — manually close the browser window to finish.")
                input("Press Enter to close the browser...")

                return "✅ Search completed."

            except Exception as e:
                return f"❌ Error during search: {e}"
            finally:
                browser.close()