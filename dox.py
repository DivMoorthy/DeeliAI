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


            except Exception as e:
                browser.close()
                return f"❌ Error locating 10-K Form Description link: {e}"

            page.wait_for_load_state("networkidle")
            Documents.dismiss_popups(page)


#tested and working up until this point 
        try:
            # Locate and click the first "Annual report" link under "Form Description"
            annual_report_link = page.locator('a', has_text="Annual report").first
            annual_report_link.wait_for(timeout=5000)
            href = annual_report_link.get_attribute('href')

            if not href:
                browser.close()
                return "❌ No 'Annual report' link found."

            # Navigate to the Annual Report page
            page.goto(f"https://www.sec.gov{href}", timeout=60000)
            print("✅ Navigated to Annual Report page.")

        except Exception as e:
            browser.close()
            return f"❌ Failed to locate or click 'Annual report': {e}"








"""
        try:
            # Click the first "Annual report" link
            annual_report_link = page.locator('a:has-text("Annual report")').first
            annual_report_link.wait_for(timeout=5000)
            annual_report_href = annual_report_link.get_attribute('href')

            if not annual_report_href:
                result = "❌ No 'Annual report' link found."
            else:
                # Navigate to the Annual Report page
                if not annual_report_href.startswith("https://"):
                    annual_report_href = "https://www.sec.gov" + annual_report_href

                print(f"🔗 Navigating to Annual Report: {annual_report_href}")
                page.goto(annual_report_href)
                page.wait_for_load_state("networkidle")
                Documents.dismiss_popups(page)

                # Save full HTML content of the page
                html_content = page.content()
                safe_cik = re.sub(r'\\W+', '_', cik_padded)
                filename = os.path.join(download_folder, f"{safe_cik}_annual_report.html")
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(html_content)

                print(f"✅ Saved HTML content to {filename}")
                result = f"✅ HTML content saved to {filename}"

        except Exception as e:
            print(f"❌ Error downloading Annual Report content: {e}")
            result = f"❌ Error downloading Annual Report content: {e}"

        finally:
            try:
                browser.close()
            except Exception:
                pass  # Avoid crashing if already closed

            return result
"""