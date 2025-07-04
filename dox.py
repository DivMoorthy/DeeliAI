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
                browser.close()
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

                # Wait for at least one row to appear after search
                rows = page.locator('[data-testid="filing-row"]')
                rows.first.wait_for(timeout=15000)






                first_link = rows.first.locator('a[data-testid="filing-details-link"]')
                first_link.wait_for(timeout=5000)
                first_link.click()
                print("✅ Clicked first 'Form Description' link after 10-K search.")

            except Exception as e:
                browser.close()
                return f"❌ Error locating 10-K Form Description link: {e}"

            page.wait_for_load_state("networkidle")
            Documents.dismiss_popups(page)

            try:
                # Wait for documents table
                page.wait_for_selector('table[data-testid="documents-table"]', timeout=10000)

                # Look for the specific document title link
                target_text = "Annual report [Section 13 and 15(d), not S-K Item 405]"
                target_link = page.locator(f'a:has-text("{target_text}")').first
                target_link.wait_for(timeout=5000)

                doc_href = target_link.get_attribute('href')
                if not doc_href:
                    browser.close()
                    return "❌ No matching 'Annual report' document link found."
                if not doc_href.startswith("https://"):
                    doc_href = "https://www.sec.gov" + doc_href

                print(f"🔗 Navigating to Annual Report Document: {doc_href}")
                page.goto(doc_href)
                Documents.dismiss_popups(page)

                # Find the first PDF link on that page
                pdf_link = page.locator('a:has-text(".pdf")').first
                pdf_href = pdf_link.get_attribute('href')
                if not pdf_href:
                    browser.close()
                    return "❌ No PDF link found on Annual Report page."
                if not pdf_href.startswith("https://"):
                    pdf_href = "https://www.sec.gov" + pdf_href

                print(f"🔗 Downloading PDF: {pdf_href}")
                response = page.request.get(pdf_href)
                if response.status != 200:
                    browser.close()
                    return "❌ Failed to download PDF document."

                safe_cik = re.sub(r'\W+', '_', cik_padded)
                filename = os.path.join(download_folder, f"{safe_cik}_annual_report.pdf")
                with open(filename, "wb") as f:
                    f.write(response.body())

                print(f"✅ Saved to {filename}")
                browser.close()
                return f"✅ Annual Report PDF saved to {filename}"

            except Exception as e:
                browser.close()
                return f"❌ Error locating or downloading report: {e}"
