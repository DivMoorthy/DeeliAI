import pdfplumber
import re

class Scraper:
    def get10kNum(pdf_path, search_term):
        """
        Extracts a numeric value near a given search term from a PDF file.

        Args:
            pdf_path (str): Path to the PDF file.
            search_term (str): Keyword to search for (case insensitive).

        Returns:
            str or None: The first numeric value found near the search term, or None if not found.
        """
        """
    ***IMPORTANT

    naming convention for the pdf is as follows from the dox file:

                    safe_cik = re.sub(r'\W+', '_', cik_padded)
                    filename = os.path.join(download_folder, f"{safe_cik}_annual_report.pdf")
                    with open(filename, "wb") as f:
                        f.write(response.body())

        """

        # Regex to find numbers with optional commas, decimals, and units like M, B, %:
        number_regex = re.compile(r'(\$?[\d,]+(?:\.\d+)?\s?(?:million|billion|M|B|%)?)', re.IGNORECASE)

        with pdfplumber.open(pdf_path) as pdf:
            # Iterate through pages
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue

                # Search term case-insensitive positions
                for match in re.finditer(re.escape(search_term), text, re.IGNORECASE):
                    start = match.start()
                    # Look around ±100 chars around search term
                    window_start = max(0, start - 100)
                    window_end = min(len(text), start + 100)
                    window_text = text[window_start:window_end]

                    # Search for numbers in window
                    nums = number_regex.findall(window_text)
                    if nums:
                        # Return first matched number near search term
                        return nums[0]

        return None
