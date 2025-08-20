import requests

def get_ticker(company_name: str):
    """
    Fetch ticker symbol from Yahoo Finance search API using company name.
    """
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={company_name}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if "quotes" in data and len(data["quotes"]) > 0:
            return data["quotes"][0]["symbol"]  # First match ticker
    except Exception as e:
        print(f"Error fetching ticker for {company_name}: {e}")
        return None
    return None


def get_yahoo_finance_link(company_name: str):
    """
    Returns Yahoo Finance link for the company if ticker is found.
    """
    ticker = get_ticker(company_name)
    if ticker:
        return f"https://finance.yahoo.com/quote/{ticker}"
    return None
