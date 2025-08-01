from api import API 
from metric import Metric
from dox import Documents
from getData import Data

class Main(API):
    def __init__(self, name, industry, valuation):
        self.name = name
        self.industry = industry
        self.valuation = int(valuation)


 #unique company number that they file under with the SEC
    
    @staticmethod
    def getCIK(ticker):
        return API.ask_LLM("What is " + ticker + "'s cik, returned as just a number no text")
    

# LLM and playwright calling helper methods

    def ask_LLM(self, prompt):
        return API.ask_LLM(prompt)

    
   
    #default value filling operation for qualitative data, currently only supports an LLM prediction
    #future implementations can pull data from similar profile companies 

    def defaultValQual(self, metric):
        val = self.ask_LLM(
            f"What is a reasonable value for the {metric} of a startup in the {self.industry} industry with a valuation of {self.valuation}"
        )
        return val
    

    # perform a similar search for the singular missing metric on a company with a similar profile 
    def defaultValQuant(self, metric):
        val = self.ask_LLM(
            f"Based on publically available data, what is a company in the " + {self.industry} + " with a valuation around " + {self.valuation} + " that would have a similar " + {metric} + " to " + {self.name} + " based on similar size, data and characteristic milestones, and what is their + {metric}?"
        )
        
        return val

        #main call for whichever metric here 
    
    
    

    #First 3 functions mainly based on quantitative data --> opt for web-scraped raw data
    #utilize the playwright API


    def sizeVal(self, link): #eps is earnings per share
        # function used to fetch data to evaluate market size and value
        EPS = Data.search_edgar_10k_viewer(link, "Earnings per share")
        EPS = float(EPS)
        if not isinstance(EPS, float):
            EPS = self.defaultValQual("Earnings per share")
        
        MDA = Data.search_edgar_10k_viewer(link, "MD&A")
        MDA = int(MDA.replace(',', ''))
        MDA = int(MDA)
        if not isinstance(MDA, int):
            MDA = self.defaultValQual("MD&A")
            

        CL = Data.search_edgar_10k_viewer(link, "customer liability")
        CL = int(CL.replace(',', ''))
        CL = int(CL)
        if not isinstance(CL, int):
            CL = self.defaultValQual("customer liability")

        return Metric.getSZMetric(EPS, MDA, CL, self.valuation)

    def growthTrends(self, link):
        RD = Data.search_edgar_10k_viewer(link, "Research and Development")
        RD = int(RD.replace(',', ''))
        RD = int(RD)
        if not isinstance(RD, int):
            RD = self.defaultValQual("Research and Development")

        OI = Data.search_edgar_10k_viewer(link, "Operating Income")
        OI = int(OI.replace(',', ''))
        OI = int(OI)
        if not isinstance(OI, int):
            OI = self.defaultValQual("Operating Income")
        
        II = Data.search_edgar_10k_viewer(link, "Investment Income")
        II = int(II.replace(',', ''))
        II = int(II)
        if not isinstance(II, int):
            OI = self.defaultValQual("Investment Income")
        

        return Metric.getGTMetric(RD, OI, II, self.valuation)

    def stratImp(self, link):
        profit_margin = Data.search_edgar_10k_viewer(link, "Gross Profit")
        profit_margin = int(profit_margin.replace(',', ''))
        profit_margin = int(profit_margin)
        if not isinstance(profit_margin, int):
            profit_margin = self.defaultValQual("Gross Profit")

        CE = Data.search_edgar_10k_viewer(link, "Cash and equivalents")
        CE = int(CE.replace(',', ''))
        CE = int(CE)
        if not isinstance(CE, int):
            CE = self.defaultValQual("Cash and equivalents")
        
        RFIR = Data.search_edgar_10k_viewer(link, "risk free interest rate")
        RFIR = int(RFIR.replace(',', ''))
        RFIR = int(RFIR)
        if not isinstance(RFIR, int):
            RFIR = self.defaultValQual("risk free interest rate")

        
            
        return Metric.getStratMetric(profit_margin, CE, RFIR, self.valuation)
    


    #returns the values in 1-10 format

    #final 3 metrics utilize mostly qualitative data --> utilize LLM to collect big-picture sentiment
    # as the design is enhanceed over time, multiple metrics can be split into both qualitative and quantitative analysis
        # generalized for now as "qualitaive data" --> usage of language prompts and LLM fetched data is ok for now         

    def compLand(self):
        newPrompt = f"Using financial analyst data, how many competitors on average does the company {self.name} have in the specific industry {self.industry}"
        activeComps = self.ask_LLM(newPrompt + " formatted as an integer value less than 5 tokens")

        comps = int(activeComps)

        if not isinstance(comps, int):
            comps = self.defaultValQual("Regulatory Constraints")
        
        return Metric.getComp(comps)

    def marketOpen(self):
        newPrompt = f"Using government and Wall Street data, evaluate the prominent regulatory constraints the {self.industry} faces "
        regConst = self.ask_LLM(newPrompt + " and rate the market openess as a number from 1 to 5 where 1 = Heavily regulated, 2 = Moderately regulated, 3 = Lightly regulated, 4 = Unregulated / gray area, 5 = Actively deregulated / tailwind, return one singular number value less thqan 5 tokens")

    
        consts = int(regConst)

        if not isinstance(consts, int):
            consts = self.defaultValQual("Regulatory Constraints")
            
        return Metric.getRegConst(consts)

        

    def intangibles(self):
        newPrompt = f"Using social media, ads, and general visibility, how much brand visibility does {self.name} have on a scale of 1-10 (10 being highest)?"
        brandVisb = self.ask_LLM(newPrompt + " formatted as an integer value less than 5 tokens")

        brandVisb = int(brandVisb)
        if not int:
            brandVisb = self.defaultValQual("Brand Visibility")
        
        return brandVisb
    
    # final score calculations done here

    def finalScore(self, link):
        print("Calculating Combined Investment Confidence Score...\n")


        #will be replaced with generalizable names when multiple metrics are introduced
        #written this way for clarity for now

        #quant
    
        SV_score = self.sizeVal(link)
        cagr_score = self.growthTrends(link)
        profit_score = self.stratImp(link)
        

        #qual
        comp_score = self.compLand()
        reg_score = self.marketOpen()
        brand_score = self.intangibles()

        
      

        # Weights for each metric — can be tuned based on priority
        weights = {
            'SV': 0.25,   # SV = size and valuation
            'cagr': 0.2,
            'profit': 0.2,
            'competition': 0.1,
            'regulation': 0.1,
            'brand': 0.15
        }

        total_score = (
            SV_score * weights['SV'] +
            cagr_score * weights['cagr'] +
            profit_score * weights['profit'] +
            comp_score * weights['competition'] +
            reg_score * weights['regulation'] +
            brand_score * weights['brand']
        )

        final = round(total_score, 2)
        print(f"\n Final Investment Confidence Score: {final}/10")
        return final
  