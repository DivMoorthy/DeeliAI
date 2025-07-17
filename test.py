from main import Main  
from dox import Documents


#cik = Main.getCIK()

# Ex for NVIDIA, expected cik = 0001045810

resultLink = Documents.getReport("1045810", headless=False)
print(resultLink)

Main.finalScore(resultLink)
# calls all 6 metric functions
# metric functions call scraper, runs on downloaded 10k
# returns values, calls metric for rating
# final calcualtions done and returns a rating 
   
#individual playwright demo test


# to fetch quantitative data for main, simply open result link, input keyword, and then fetch data 

