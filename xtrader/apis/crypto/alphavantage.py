import requests, json

from xtrader.apis.crypto.base import BaseCryptoAPI

OUTPUT_SIZES = ['compact', 'full']
DATA_TYPES = ['json', 'csv']
INTRADAY_INTERVALS = ['1min', '5min', '15min', '30min', '60min']


class AlphaVantageCryptoAPI(BaseCryptoAPI):

    def __init__(self, api_key):
        self.api_key = api_key


    def call_api(self, endpoint: str) -> json:
        response = requests.get(endpoint)
        if response.status_code != 200:
            raise ValueError(f'Invalid API response: {response}')
        return response
    

    def get_exchange_rate(self, from_currency: str, to_currency: str) -> json:
        """ This API returns the realtime exchange rate for any pair of digital currency
          (e.g., Bitcoin) or physical currency (e.g., USD).
        """
        endpoint = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={self.api_key}"
        return self.call_api(endpoint)
    

    def get_intraday(self, symbol: str, market: str, interval: str,
                        outputsize: str='compact', datatype: str='json') -> json:
        """
        Returns intraday time series (timestamp, open, high, low, close, volume)
        of the cryptocurrency specified, updated realtime.
        """
        if outputsize not in OUTPUT_SIZES:
            raise ValueError(f'`outputsize` must be one of: {outputsize}')
        if datatype not in DATA_TYPES:
            raise ValueError(f'`datatype` must be one of: {datatype}')
        if interval not in INTRADAY_INTERVALS:
            raise ValueError(f'`interval` must be one of: {interval}')
        
        endpoint = f"https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol={symbol}&market={market}&interval={interval}"
        if outputsize == 'full':
            endpoint += '&outputsize=full'
        if datatype == 'csv':
            endpoint += '&datatype=csv'
        endpoint += f"&apikey={self.api_key}"

        return self.call_api(endpoint)
    

    def get_daily(self, symbol: str, market: str) -> json:
        """ 
        Returns the daily historical time series for a digital currency
        (e.g., BTC) traded on a specific market (e.g., CNY/Chinese Yuan), refreshed daily at midnight (UTC).
        Prices and volumes are quoted in both the market-specific currency and USD.
        """
        endpoint = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market={market}&apikey={self.api_key}"
        return endpoint
        return self.call_api(endpoint)
    
    
    def get_weekly(self, symbol: str, market: str) -> json:
        """ 
        Returns the weekly historical time series for a digital currency
        (e.g., BTC) traded on a specific market (e.g., CNY/Chinese Yuan), refreshed daily at midnight (UTC).
        Prices and volumes are quoted in both the market-specific currency and USD.
        """
        endpoint = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_WEEKLY&symbol={symbol}&market={market}&apikey={self.api_key}"
        return self.call_api(endpoint)
    

    def get_monthly(self, symbol: str, market: str) -> json:
        """ 
        Returns the monthly historical time series for a digital currency
        (e.g., BTC) traded on a specific market (e.g., CNY/Chinese Yuan), refreshed daily at midnight (UTC).
        Prices and volumes are quoted in both the market-specific currency and USD.
        """
        endpoint = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol={symbol}&market={market}&apikey={self.api_key}"
        return self.call_api(endpoint)