import requests
import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

def get_stock_price(ticker : str):
    url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()

        current = data.get("c")
        previous = data.get("pc")
        if current is None or previous is None:
            return None  , None , None
        change = np.round(current - previous , 2)
        up_down = "up" if change > 0 else ("down" if change < 0 else "neutral")

        return current , change , up_down
    except Exception as e:
        print("Errror fetching price : ")
        return None , None , None
print(FINNHUB_API_KEY)
