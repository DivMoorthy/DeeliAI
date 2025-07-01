from main import Main  
from web_scrape import Playwright
from dox import Documents


#cik = Main.getCIK("NVDA")

# Example CIK for NVIDIA = 0001045810
result = Documents.getReport("1045810", headless=False)
print(result)