from api import API 
from web_scrape import Playwright
from metric import Metric

class Main(API):
    def __init__(self, name, industry, valuation):
        self.name = name
        self.industry = industry
        self.valuation = valuation


# LLM and playwright calling helper methods

    def ask_LLM(self, prompt):
        return API.ask_LLM(prompt)

    def scrape_metric(self, metric):
        result = Playwright.scrape_metric(self.name, metric)
        return result or self.defaultVal(metric)
    
    
    #default value filling operation, currently only supports an LLM prediction
    #future implementations can pull data from similar profile companies 

    def defaultVal(self, metric):
        val = self.ask_LLM(
            f"What is a reasonable value for the {metric} of a startup in the {self.industry} industry with a valuation of {self.valuation}"
        )
        return val
    
    

    #First 3 functions mainly based on quantitative data --> opt for web-scraped raw data
    #utilize the playwright API


    def sizeVal(self):
        TAM = self.scrape_metric("TAM") # call to playwright
        print(f"TAM: {TAM}")
        return Metric.getTAMMetric(TAM)

    def growthTrends(self):
        CAGR = self.scrape_metric("CAGR") # call to playwright
        print(f"CAGR: {CAGR}") 
        return Metric.getCAGRMetric(CAGR)
    
    #experimental trial with specialized metric scraper rather than generalizable one

    def stratImp(self):
        profit_margin = Playwright.scrape_10k_profit_margin(self.name)
        print(f"Profit Margin for {self.name}: {profit_margin}")
        return Metric.getProfitMetric(profit_margin)

    #returns the values in 1-10 format

    #final 3 metrics utilize mostly qualitative data --> utilize LLM to collect big-picture sentiment
    # as the design is enhanceed over time, multiple metrics can be split into both qualitative and quantitative analysis
        # generalized for now as "qualitaive data" --> usage of language prompts and LLM fetched data is ok for now         

    def compLand(self):
        newPrompt = f"Using financial analyst data, how many competitors on average does the company {self.name} have in the specific industry {self.industry}"
        activeComps = self.ask_LLM(newPrompt + " formatted as an integer value less than 5 tokens")

        if not isinstance(activeComps, int):
            activeComps = self.defaultVal("Active Competitors")
        
        return Main.getComp(activeComps)

    def marketOpen(self):
        newPrompt = f"Using government and Wall Street data, how many prominent regulatory constraints does a startup in the {self.industry} face?"
        regConst = self.ask_LLM(newPrompt + " formatted as an integer value less than 5 tokens and evaluate regulatory investment confidence from a numeric scale: 1 = Heavily regulated, 2 = Moderately regulated, 3 = Lightly regulated, 4 = Unregulated / gray area, 5 = Actively deregulated / tailwind")

        if not isinstance(regConst, int):
            regConst = self.defaultVal("Regulatory Constraints")

        return Main.getRegConst(regConst)

        

    def intangibles(self):
        newPrompt = f"Using social media, ads, and general visibility, how much brand visibility does {self.name} have on a scale of 1-10 (10 being highest)?"
        brandVisb = self.ask_LLM(newPrompt + " formatted as an integer value less than 5 tokens")

        if not isinstance(brandVisb, int):
            brandVisb = self.defaultVal("Brand Visibility")
        
        return brandVisb
    
    # final score calculations done here

    def finalScore(self):
        print("Calculating Combined Investment Confidence Score...\n")


        #will be replaced with generalizable names when multiple metrics are introduced
        #written this way for clarity for now

        tam_score = self.sizeVal()
        cagr_score = self.growthTrends()
        profit_score = self.stratImp()
        comp_score = self.compLand()
        reg_score = self.marketOpen()
        brand_score = self.intangibles()

        # Weights for each metric — can be tuned based on priority
        weights = {
            'tam': 0.2,
            'cagr': 0.2,
            'profit': 0.15,
            'competition': 0.15,
            'regulation': 0.15,
            'brand': 0.15
        }

        total_score = (
            tam_score * weights['tam'] +
            cagr_score * weights['cagr'] +
            profit_score * weights['profit'] +
            comp_score * weights['competition'] +
            reg_score * weights['regulation'] +
            brand_score * weights['brand']
        )

        final = round(total_score, 2)
        print(f"\n Final Investment Confidence Score: {final}/10")
        return final