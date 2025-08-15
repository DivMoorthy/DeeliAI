import requests
from bs4 import BeautifulSoup

def get_tam_yahoo(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}/profile"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Example: Search for TAM data in the 'Profile' section
    tam_data = soup.find('span', text='Total Addressable Market')
    if tam_data:
        return tam_data.find_next('span').text
    return "TAM data not found"

