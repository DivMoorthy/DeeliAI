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
            except:
                pass

    def getReport(cik, download_folder="downloads", headless=True):
        os.makedirs(download_folder, exist_ok=True)
        cik_padded = cik.zfill(10)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless, slow_mo=100)
            page = browser.new_page()

            # 1. Navigate to company CIK page
            base_url = f"https://www.sec.gov/edgar/browse/?CIK={cik_padded}"
            print(f"🔍 Navigating to {base_url}")
            page.goto(base_url)
            Documents.dismiss_popups(page)

            # 2. Click the "View Filings" button
            try:
                page.wait_for_selector('a[data-testid="view-filings-tab"]', timeout=10000)
                page.locator('a[data-testid="view-filings-tab"]').click()
                print("✅ Clicked 'View Filings' tab.")
            except TimeoutError:
                browser.close()
                return "❌ 'View Filings' tab not found or not clickable."
            
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)

            # 3. Try to apply filter: "Annual and Quarterly Reports"
            try:
                filter_button = page.locator('button[data-testid="filter-button"]')
                if filter_button.is_visible():
                    filter_button.click()
                    page.wait_for_selector('ul[role="listbox"] li', timeout=5000)
                    page.locator('ul[role="listbox"] li', has_text="Annual and Quarterly Reports").first.click()
                    print("✅ Filter applied: Annual and Quarterly Reports")
                    page.wait_for_load_state("networkidle")
                    page.wait_for_timeout(2000)
            except Exception as e:
                print(f"⚠️  Filter not applied: {e}")

            # 4. Wait for filings list
            try:
                page.wait_for_selector('[data-testid="filing-row"]', timeout=15000)
            except TimeoutError:
                browser.close()
                return "❌ No filings found or page took too long to load."

            filings = page.locator('[data-testid="filing-row"]')
            if filings.count() == 0:
                browser.close()
                return "❌ No filings listed."

            print("✅ Filings loaded. Proceeding...")

            # 5. Click first filing detail link
            filings.nth(0).locator('a[data-testid="filing-details-link"]').click()

            # 6. Wait for document links
            try:
                page.wait_for_selector('a[data-testid="document-link"]', timeout=10000)
            except TimeoutError:
                browser.close()
                return "❌ No document links found on filing detail page."

            doc_link = page.locator('a[data-testid="document-link"]').first.get_attribute("href")
            if not doc_link:
                browser.close()
                return "❌ No document link found."

            if not doc_link.startswith("https://"):
                doc_link = "https://www.sec.gov" + doc_link

            # 7. Navigate to document and download content
            page.goto(doc_link)
            Documents.dismiss_popups(page)

            content = page.content()
            safe_cik = re.sub(r'\W+', '_', cik_padded)
            filename = os.path.join(download_folder, f"{safe_cik}_latest_10k.html")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)

            browser.close()
            return f"✅ Report saved to {filename}"



