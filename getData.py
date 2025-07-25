from playwright.sync_api import sync_playwright
import os
import re
import time


class Data:
    @staticmethod
    def search_edgar_10k_viewer(url: str, keyword: str) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=75)
            page = browser.new_page()
            try:
                print("🌐 Navigating to SEC iXBRL viewer...")
                page.goto(url, timeout=60000)
                page.wait_for_load_state("networkidle")

                # Wait for iframe to be attached and loaded
                page.wait_for_selector('iframe#ixvFrame', timeout=15000)
                iframe = page.frame(name="ixvFrame")
                if not iframe:
                    raise Exception("❌ Unable to access iframe named 'ixvFrame'")

                print("✅ Accessed iframe 'ixvFrame'.")

                # Locate input using placeholder text
                search_input = iframe.locator('input[placeholder="Search Facts"]')
                search_input.wait_for(timeout=10000)
                print("✅ Located 'Search Facts' input.")

                # Click and type keyword slowly
                search_input.click()
                for char in keyword:
                    search_input.type(char)
                    time.sleep(0.15)

                search_input.press("Enter")
                print(f"⌨️ Typed '{keyword}' and pressed Enter.")

                # Wait for dropdown list
                dropdown_items = iframe.locator('div.autocomplete-list div')
                dropdown_items.first.wait_for(timeout=5000)

                first_result = dropdown_items.first.inner_text()
                print(f"🔎 First dropdown result: {first_result}")
                return first_result

            except Exception as e:
                print(f"❌ Error: {e}")
                return None

            finally:
                input("Press Enter to close the browser...")
                browser.close()
