from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import time

class Playwright:
    @staticmethod
    def scrape_metric(company_name, metric):
        def extract_number(text):
            match = re.search(r'(\d{1,3}(?:\.\d+)?%)', text)
            return match.group(1) if match else None

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            search_url = f"https://www.sec.gov/edgar/search/#/q={company_name}%2010-k&filter_forms=10-K"
            page.goto(search_url)
            page.wait_for_selector("table")

            time.sleep(2)
            first_link = page.locator("table a").first
            href = first_link.get_attribute("href")
            if not href:
                browser.close()
                return None

            doc_page_url = "https://www.sec.gov" + href
            page.goto(doc_page_url)
            page.wait_for_load_state("networkidle")

            doc_link = page.locator("a:has-text('10-K')").first
            doc_href = doc_link.get_attribute("href")
            if not doc_href:
                browser.close()
                return None

            full_doc_url = "https://www.sec.gov" + doc_href
            page.goto(full_doc_url)
            page.wait_for_load_state("networkidle")

            soup = BeautifulSoup(page.content(), "html.parser")
            text = soup.get_text(separator=" ")

            browser.close()

            return extract_number(text)
        
    def scrape_10k_profit_margin(company_name):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

            # 📌 Stable, known NVIDIA 10-K filing (Jan 2023)
            known_10k_url = "https://www.sec.gov/Archives/edgar/data/1045810/000104581023000034/nvda-20230129.htm"

            try:
                page.goto(known_10k_url, timeout=60000)
                page.wait_for_load_state("networkidle")
            except:
                print("❌ Could not load the known 10-K document.")
                browser.close()
                return None

            soup = BeautifulSoup(page.content(), "html.parser")
            text = soup.get_text(separator=" ")

            browser.close()

            # 🧠 Improved regex
            pattern = r"(?:gross|operating|net)?\s*(?:profit\s*)?margin[s]?\s*(?:was|were|of|stood at|:|–|-|=)?\s*([\d]{1,3}(?:\.\d+)?\s?%)"
            matches = re.findall(pattern, text, re.IGNORECASE)

            if matches:
                print("🔍 Matches found:", matches[:5])  # Show top few matches
                return matches[0]

            return "Profit margin not found."
   
        
    