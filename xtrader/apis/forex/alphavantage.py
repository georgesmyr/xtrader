import requests, json
from typing import Optional
from xtrader.utils import call_api

class AlphaVantageForexAPI:

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_exchange_rate(self, from_currency: str, to_currency: str) -> json:
        """
        Returns the realtime exchange rate for a pair of digital currency (e.g., Bitcoin) and physical currency (e.g., USD).
        """
        endpoint = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={self.api_key}"
        return call_api(endpoint)
    
    