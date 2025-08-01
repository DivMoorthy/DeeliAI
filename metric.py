
#rankings for the first three quantitiative metrics 

class Metric:
    @staticmethod
    def getSZMetric(EPS, MDA, CL, valuation):

        # calculation formula is [EPS x (1 + CL/MC)] / [LTD/MC + c]
        #logic:
        # High EPS implies profitability and value to shareholders.
        # Higher CL/MC is good because it reflects prepaid demand or strong customer commitment.
        # Higher LTD/MC is negative, showing increased leverage risk.
        # So the FSP Ratio rewards profitability and demand while penalizing debt.
        """
        EPS: Earnings per Share
        MDA: Long-Term Debt (excluding current maturities)
        CL: Customer Liabilities
        valuation: Market Capitalization
        
        Returns: Integer score from 1 to 10
        """
        
        epsilon = 1e-6  # avoid division by zero

        if valuation <= 0:
            return 1  # default to worst score if valuation invalid

        # Calculate FSP ratio
        fsp = (EPS * (1 + (CL / valuation))) / ((MDA / valuation) + epsilon)

        # Bin FSP ratio into score from 1 to 10
        if fsp < 1:
            score = 1
        elif fsp < 2:
            score = 2
        elif fsp < 4:
            score = 3
        elif fsp < 7:
            score = 4
        elif fsp < 12:
            score = 5
        elif fsp < 20:
            score = 6
        elif fsp < 35:
            score = 7
        elif fsp < 60:
            score = 8
        elif fsp < 100:
            score = 9
        else:
            score = 10

        return score


    def getRDMetric(rd_exp):
        if rd_exp < 1000:
            score = 1
        elif rd_exp < 10000:
            score = 3
        elif rd_exp < 1000000:
            score = 5
        elif rd_exp < 10000000:
            score = 7
        elif rd_exp < 1000000000:
            score = 9
        else:
            score = 10
        return score

    def getProfitMetric(margin_percent):
        if margin_percent < 0:
            score = 1
        elif margin_percent < 5:
            score = 3
        elif margin_percent < 15:
            score = 5
        elif margin_percent < 25:
            score = 7
        elif margin_percent < 40:
            score = 9
        else:
            score = 10
        return score

    #rankings for the qualitative metrics using bin-style evaluations as well

    def getComp(num_competitors):
        if num_competitors == 0:
            score = 2
        elif num_competitors <= 2:
            score = 4
        elif num_competitors <= 5:
            score = 6
        elif num_competitors <= 15:
            score = 8
        elif num_competitors <= 30:
            score = 6
        else:
            score = 3
        return score
        
    def getRegConst(regulation_level: int) -> int:
        """
        Evaluate regulatory investment confidence from a numeric scale:
        1 = Heavily regulated
        2 = Moderately regulated
        3 = Lightly regulated
        4 = Unregulated / gray area
        5 = Actively deregulated / tailwind
        """
        if regulation_level == 1:
            return 2
        elif regulation_level == 2:
            return 5
        elif regulation_level == 3:
            return 8
        elif regulation_level == 4:
            return 6
        elif regulation_level == 5:
            return 9
        else:
            return 5  # default neutral score if input is unexpected