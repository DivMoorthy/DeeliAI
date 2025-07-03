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
                search_input = page.locator('input[placeholder="Search table"]')
                search_input.fill("10-K")
                print("✅ Entered '10-K' in search table.")
                page.wait_for_timeout(2000)

                first_row = page.locator('[data-testid="filing-row"]').first
                first_row.wait_for(timeout=15000)
                print("✅ Found first filtered filing row.")
            except:
                browser.close()
                return "❌ No filings found after searching for 10-K."

            first_row.locator('a[data-testid="filing-details-link"]').click()

            page.wait_for_load_state("networkidle")
            Documents.dismiss_popups(page)

            try:
                page.wait_for_selector('table[data-testid="documents-table"]', timeout=10000)
                doc_table = page.locator('table[data-testid="documents-table"]')
                annual_report_link = doc_table.locator('a:has-text("Annual Report")').first
                annual_report_link.wait_for(timeout=5000)

                doc_href = annual_report_link.get_attribute('href')
                if not doc_href:
                    browser.close()
                    return "❌ No 'Annual Report' link found."
                if not doc_href.startswith("https://"):
                    doc_href = "https://www.sec.gov" + doc_href

                print(f"🔗 Navigating to Annual Report: {doc_href}")
                page.goto(doc_href)
                Documents.dismiss_popups(page)

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

                safe_cik = re.sub(r'\\W+', '_', cik_padded)
                filename = os.path.join(download_folder, f"{safe_cik}_annual_report.pdf")
                with open(filename, "wb") as f:
                    f.write(response.body())

                print(f"✅ Saved to {filename}")
                browser.close()
                return f"✅ Annual Report PDF saved to {filename}"

            except Exception as e:
                browser.close()
                return f"❌ Error getting Annual Report PDF: {e}"
