import requests
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("FINNHUB_API_KEY")


def fetch_news(category = "general"):
    url = f"https://finnhub.io/api/v1/news?category=general&token={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code}")
    return response.json()



    
