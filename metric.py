
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


    def getGTMetric(RD, OI, II, valuation):
        """
        Returns a score from 1 to 10 that estimates company growth strength.
        
        RD = Research and Development expenses
        OI = Operating Income
        II = Investment Income
        valuation = Market Capitalization (in same units as above)

        All values should be in consistent currency (e.g., USD).
        """
        if valuation <= 0:
            return 1  # default to lowest score on invalid valuation

        # Normalize and weight each component
        w1, w2, w3 = 0.4, 0.5, 0.1
        gtr = (
            (RD / valuation) * w1 +
            (OI / valuation) * w2 +
            (II / valuation) * w3
        )

        # Scale GTR and bin into scores
        if gtr < 0.001:
            return 1
        elif gtr < 0.002:
            return 2
        elif gtr < 0.004:
            return 3
        elif gtr < 0.007:
            return 4
        elif gtr < 0.012:
            return 5
        elif gtr < 0.020:
            return 6
        elif gtr < 0.035:
            return 7
        elif gtr < 0.060:
            return 8
        elif gtr < 0.1:
            return 9
        else:
            return 10

    def getStratMetric(profit_margin, CE, RFIR, valuation):
        """
        Calculates a 1-10 strategic importance score.

        profit_margin: company profit margin as a decimal (e.g., 0.25 for 25%)
        CE: cash and cash equivalents (absolute value)
        RFIR: risk-free interest rate as a decimal (e.g., 0.04 for 4%)
        valuation: market capitalization (absolute value)

        Returns an integer score from 1 to 10.
        """
        if valuation <= 0 or RFIR <= 0:
            return 1  # fallback on invalid input

        w1, w2 = 0.6, 0.4  # weights for profit margin and cash adjusted by RFIR

        # Normalize profit margin by weighting directly (already a ratio)
        pm_score = profit_margin * w1

        # Cash adjusted by valuation and RFIR
        cash_score = (CE / valuation) * (1 / RFIR) * w2

        # Composite strategic importance score
        sis = pm_score + cash_score

        # Bin into 1-10 scale
        if sis < 0.02:
            return 1
        elif sis < 0.04:
            return 2
        elif sis < 0.06:
            return 3
        elif sis < 0.08:
            return 4
        elif sis < 0.1:
            return 5
        elif sis < 0.12:
            return 6
        elif sis < 0.15:
            return 7
        elif sis < 0.18:
            return 8
        elif sis < 0.22:
            return 9
        else:
            return 10
            

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