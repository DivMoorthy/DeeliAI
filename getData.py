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

                # Wait for fact list items to appear in the sidebar
                iframe.wait_for_selector('a.list-group-item', timeout=5000)

                # Locate the first result item
                first_fact = iframe.locator('a.list-group-item').first

                # Wait for it to be ready
                first_fact.wait_for(timeout=5000)

                # Extract the numeric value
                numeric_value = first_fact.locator('[data-cy="factVal"]').inner_text()

                print(f"🔢 First fact value: {numeric_value}")
                return numeric_value
            
            except Exception as e:
                return {"error": f"❌ Error: {str(e)}"}

            finally:
                browser.close()