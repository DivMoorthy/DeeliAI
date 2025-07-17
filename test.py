from main import Main  
from scrape import Scraper
from dox import Documents



# Ex for NVIDIA, expected cik = 0001045810

#Main.downloadData("NVDA")
#gets cik,calls dox which downloads the 10k and puts into local folder
#calls Documents.getReport("1045810", headless=False)

#Main.finalScore()
# calls all 6 metric functions
# metric functions call scraper, runs on downloaded 10k
# returns values, calls metric for rating
# final calcualtions done and returns a rating 
   
#individual playwright demo test

result = Documents.getReport("1045810", headless=False)
print(result)


