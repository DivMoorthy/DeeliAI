from playwright.sync_api import sync_playwright, TimeoutError
import os
import re

class Documents:
    def dismiss_popups(page):
        popup_selectors = [
            'button#onetrust-accept-btn-handler',
            'button[aria-label="Close"]',
            'button.cookie-consent-accept',
            'div#consent-banner button.accept',
        ]
        for selector in popup_selectors:
            try:
                page.locator(selector).click(timeout=2000)
                print(f"Dismissed popup: {selector}")
            except:
                pass

    def getReport(cik, download_folder="downloads", headless=True):
        os.makedirs(download_folder, exist_ok=True)
        cik_padded = cik.zfill(10)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless, slow_mo=50)
            page = browser.new_page()

            base_url = f"https://www.sec.gov/edgar/browse/?CIK={cik_padded}"
            print(f"🔍 Navigating to {base_url}")
            page.goto(base_url, timeout=60000)
            Documents.dismiss_popups(page)

            try:
                if page.locator('a[data-testid="view-filings-tab"]').is_visible():
                    page.locator('a[data-testid="view-filings-tab"]').click()
                else:
                    page.get_by_text("View Filings").click()
                print("✅ Clicked 'View Filings'.")
            except Exception as e:
                return f"❌ Failed to click 'View Filings': {e}"

            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)

            try:
                # Clear date filter if present
                date_input = page.locator('input[placeholder="From Date (yyyy-mm-dd)"]')
                date_input.fill("")

                # Search for 10-K filings
                search_input = page.locator('input[placeholder="Search table"]')
                search_input.click()
                search_input.fill("")  # clear any pre-existing text
                search_input.type("10-K", delay=100)
                search_input.press("Enter")

                print("✅ Typed and submitted '10-K' in search table.")
                page.wait_for_timeout(3000)


            except Exception as e:
                return f"❌ Error locating 10-K Form Description link: {e}"

            page.wait_for_load_state("networkidle")
            Documents.dismiss_popups(page)


#tested and working up until this point 
        
        # 4. Now click the first actual document link (class="document-link")
        
            try:
                # Wait for at least one document link to appear
                page.wait_for_selector('a.document-link', timeout=5000)

                # Grab the first matching link safely
                doc_link = page.locator('a.document-link:has-text("Annual report [Section 13 and 15(d), not S-K Item 405]")').first

                # Use get_attribute — it's fine in sync mode as long as context is alive
                href = doc_link.get_attribute('href')

                if href:
                    full_url = f"https://www.sec.gov{href}"
                    print(f"✅ Navigating to 10-K report: {full_url}")
                    page.goto(full_url, timeout=60000)
                    page.wait_for_timeout(5000)


                    current_url = page.url

                    # You can print or save it to a file
                    print(f"✅ Current URL: {current_url}")
                    return current_url

            
            except Exception as e:
                print(f"❌ Error downloading Annual Report content: {e}")
                result = f"❌ Error downloading Annual Report content: {e}"



