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
                page.wait_for_selector(selector, timeout=2000)
                page.locator(selector).click()
                print(f"Dismissed popup: {selector}")
            except TimeoutError:
                pass

    def getReport(cik, download_folder="downloads", headless=True):
        os.makedirs(download_folder, exist_ok=True)

        if not cik.isdigit():
            raise ValueError("CIK must be numeric string without leading 'CIK' prefix")

        # Pad CIK to 10 digits (SEC format)
        cik_padded = cik.zfill(10)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            page = browser.new_page()

            # Open SEC new filing browser for this CIK
            base_url = f"https://www.sec.gov/edgar/browse/?CIK={cik_padded}"
            print(f"Navigating to {base_url}")
            page.goto(base_url)

            Documents.dismiss_popups(page)

            # Wait for the filter dropdown to appear, then select "Annual and Quarterly Reports"
            try:
                # Click the filter dropdown
                page.wait_for_selector('button[data-testid="filter-button"]', timeout=10000)
                page.locator('button[data-testid="filter-button"]').click()

                # Wait for the filter menu items to appear
                page.wait_for_selector('ul[role="listbox"] li', timeout=5000)

                # Click the "Annual and Quarterly Reports" filter option
                # The filter text might be exactly "Annual and Quarterly Reports"
                option_locator = page.locator('ul[role="listbox"] li', has_text="Annual and Quarterly Reports").first
                option_locator.click()
            except TimeoutError:
                print("Filter dropdown or option not found - proceeding without filter")

            # Wait for filings list to update after filter
            page.wait_for_timeout(3000)

            # Wait for the filing rows to appear (list items with data-testid="filing-row")
            page.wait_for_selector('[data-testid="filing-row"]', timeout=10000)
            filings = page.locator('[data-testid="filing-row"]')
            filing_count = filings.count()

            if filing_count == 0:
                browser.close()
                return f"No filings found for CIK {cik_padded}."

            # Click the first filing to go to its detail page
            filings.nth(0).locator('a[data-testid="filing-details-link"]').click()

            # Wait for filing detail page to load main document list
            page.wait_for_selector('a[data-testid="document-link"]', timeout=10000)

            # Get the first document link (usually the main filing document)
            doc_link = page.locator('a[data-testid="document-link"]').first.get_attribute("href")

            if not doc_link:
                browser.close()
                return "No document link found on filing detail page."

            # Build full URL if relative
            if not doc_link.startswith("https://"):
                doc_link = "https://www.sec.gov" + doc_link

            # Navigate to the document page and get content
            page.goto(doc_link)
            Documents.dismiss_popups(page)

            content = page.content()

            safe_cik = re.sub(r'\W+', '_', cik_padded)
            filename = os.path.join(download_folder, f"{safe_cik}_latest_report.html")

            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)

            browser.close()
            return f"Latest report downloaded and saved to {filename}"



