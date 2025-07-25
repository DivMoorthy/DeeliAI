from main import Main  
from dox import Documents
from getData import Data

#*******cik = Main.getCIK("NVDA")

#print(cik)
#tested and working
# Ex for NVIDIA, expected cik = 0001045810

#*******resultLink = Documents.getReport(cik, headless=False)

resultLink = "https://www.sec.gov/ix?doc=/Archives/edgar/data/0001045810/000104581025000023/nvda-20250126.htm"
#print(resultLink)
#tested and working as well 

client = Main("NVDA", "semiconductors", "100B")

#Main.finalScore(client, resultLink)
#print(Main.intangibles(client))
#all qual metrics tested and working

Data.search_edgar_10k_viewer(resultLink, "profit")


# calls all 6 metric functions
# metric functions call scraper, runs on downloaded 10k
# returns values, calls metric for rating
# final calcualtions done and returns a rating 
   


