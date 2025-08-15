# main.py
from api import API
import re

def classify_industry_sector(keyword: str) -> str:
    """Classifies an industry keyword into an S&P 500 sector."""
    keyword = keyword.lower().strip()
    sector_keywords = {
        "Information Technology": [
            "software", "semiconductor", "cloud", "artificial intelligence",
            "chip manufacturing", "it services", "cybersecurity", "data analytics"
        ],
        "Health Care": [
            "pharmaceuticals", "hospital", "biotechnology", "medical devices",
            "healthcare services", "diagnostics", "life sciences"
        ],
        "Financials": [
            "banking", "insurance", "asset management", "investment banking",
            "brokerage", "mortgage", "financial services", "credit services"
        ],
        "Energy": [
            "oil", "gas", "pipeline", "renewable energy", "solar",
            "wind power", "drilling", "energy infrastructure"
        ],
        "Consumer Discretionary": [
            "retail", "luxury goods", "automotive", "entertainment",
            "restaurants", "leisure products", "homebuilding", "travel"
        ],
        "Consumer Staples": [
            "grocery", "beverage", "food products", "household goods",
            "personal care products", "packaged foods", "tobacco"
        ],
        "Industrials": [
            "manufacturing", "construction", "transportation", "aerospace",
            "defense", "engineering", "industrial machinery", "logistics"
        ],
        "Materials": [
            "mining", "chemicals", "metals", "steel production",
            "paper products", "building materials", "packaging materials"
        ],
        "Real Estate": [
            "reit", "real estate investment", "property management",
            "commercial real estate", "residential real estate", "land development"
        ],
        "Utilities": [
            "electric", "water", "natural gas", "power generation",
            "nuclear energy", "waste management", "energy distribution"
        ],
        "Communication Services": [
            "telecommunications", "media", "advertising", "streaming",
            "broadcasting", "wireless services", "publishing"
        ]
    }

    for sector, keywords in sector_keywords.items():
        if any(k in keyword for k in keywords):
            return sector
    return "Unknown"


def get_sector_performance_from_gemini(sector_name: str) -> str:
    """Get S&P 500 sector performance using the API.ask_LLM method."""
    if sector_name == "Unknown":
        return None

    prompt = f"Give me the current S&P 500 {sector_name} sector daily percentage change, only return the number with a % sign."
    response = API.ask_LLM(prompt)

    # Extract % number using regex
    match = re.search(r"([\+\-]?\d+\.\d+%)", response)
    if match:
        return match.group(1)
    else:
        raise ValueError(f"Could not extract percentage from API response: {response}")


def map_performance_to_score(perf_str: str) -> float:
    """Convert performance percentage to a score from 1 to 10."""
    perf_value = float(perf_str.replace('%', ''))
    min_perf, max_perf = -5.0, 5.0
    clipped_perf = max(min_perf, min(max_perf, perf_value))
    score = 1 + (clipped_perf - min_perf) * (9 / (max_perf - min_perf))
    return round(score, 1)


def get_investment_score_for_industry(industry_keyword: str) -> dict:
    """Classify the industry, get performance via Gemini API, and return score."""
    sector = classify_industry_sector(industry_keyword)
    if sector == "Unknown":
        return {"sector": sector, "performance": None, "score": None}

    perf_str = get_sector_performance_from_gemini(sector)
    score = map_performance_to_score(perf_str)

    return {
        "sector": sector,
        "performance": perf_str,
        "score": score
    }


# --- Example call ---
if __name__ == "__main__":
    industry = "renewable energy"
    result = get_investment_score_for_industry(industry)
    print(result)
