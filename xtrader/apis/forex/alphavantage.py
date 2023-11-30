import requests, json
from typing import Optional
from xtrader.utils import call_api

OUTPUT_SIZES = ['compact', 'full']
DATA_TYPES = ['json', 'csv']
INTRADAY_INTERVALS = ['1min', '5min', '15min', '30min', '60min']

class AlphaVantageForexAPI:

    def __init__(self, api_key: str):
        self.api_key = api_key


    def get_exchange_rate(self, from_symbol: str, to_symbol: str) -> json:
        """
        Returns the realtime exchange rate for a pair of digital currency (e.g., Bitcoin) and physical currency (e.g., USD).
        :param from_currency: The currency you would like to get the exchange rate for.
                              It can either be a physical currency or digital/crypto currency.
        :param to_currency:   The destination currency for the exchange rate. It can either be a physical currency or digital/crypto currency. 
        """
        endpoint = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_symbol}&to_currency={to_symbol}&apikey={self.api_key}"
        return call_api(endpoint)
    
    
    def get_intraday(self, from_symbol: str, to_symbol: str, interval: str,
                    outputsize: str = 'compact', datatype: str = 'json') -> json:
        """
        Returns intraday time series (timestamp, open, high, low, close) of the FX currency pair specified, updated realtime.
        :param interval: Time interval between two consecutive data points in the time series.
                         The following values are supported: 1min, 5min, 15min, 30min, 60min
        :param outputsize: `compact` returns only the latest 100 data points in the intraday time series;`full` returns the full-length intraday time series. 
                           The `compact` option is recommended if you would like to reduce the data size of each API call.
        :param datatype: `json` returns the intraday time series in JSON format; `csv` returns the time series as a CSV (comma separated value) file.
        """
        if interval not in INTRADAY_INTERVALS:
            raise ValueError(f"interval must be one of {INTRADAY_INTERVALS}")
        if outputsize not in OUTPUT_SIZES:
            raise ValueError(f"outputsize must be one of {OUTPUT_SIZES}")
        if datatype not in DATA_TYPES:
            raise ValueError(f"datatype must be one of {DATA_TYPES}")
        
        endpoint = f"https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol={from_symbol}&to_symbol={to_symbol}&interval={interval}"
        if outputsize == 'full':
            endpoint += f"&outputsize={outputsize}"
        if datatype == 'csv':
            endpoint += f"&datatype={datatype}"
        endpoint += f"&apikey={self.api_key}"

        return call_api(endpoint)


    def get_daily(self, from_symbol: str, to_symbol: str, outputsize: str = 'compact', datatype: str = 'json') -> json:
        """ 
        Returns the daily time series (timestamp, open, high, low, close) of the FX currency pair specified, updated realtime.
        :param outputsize: `compact` returns only the latest 100 data points in the intraday time series;`full` returns the full-length intraday time series. 
                           The `compact` option is recommended if you would like to reduce the data size of each API call.
        :param datatype: `json` returns the intraday time series in JSON format; `csv` returns the time series as a CSV (comma separated value) file.
        """

        if outputsize not in OUTPUT_SIZES:
            raise ValueError(f"outputsize must be one of {OUTPUT_SIZES}")
        if datatype not in DATA_TYPES:
            raise ValueError(f"datatype must be one of {DATA_TYPES}")
        
        endpoint = f"https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={from_symbol}&to_symbol={to_symbol}"
        if outputsize == 'full':
            endpoint += f"&outputsize={outputsize}"
        if datatype == 'csv':
            endpoint += f"&datatype={datatype}"
        endpoint += f"&apikey={self.api_key}"

        return call_api(endpoint)
    

    def get_weekly(self, from_symbol: str, to_symbol: str, datatype: str = 'json') -> json:
        """
        Returns the weekly time series (timestamp, open, high, low, close) of the FX currency pair specified, updated realtime.
        :param datatype: `json` returns the intraday time series in JSON format; `csv` returns the time series as a CSV (comma separated value) file.
        """

        if datatype not in DATA_TYPES:
            raise ValueError(f"datatype must be one of {DATA_TYPES}")
        
        endpoint = f"https://www.alphavantage.co/query?function=FX_WEEKLY&from_symbol={from_symbol}&to_symbol={to_symbol}"
        if datatype == 'csv':
            endpoint += f"&datatype={datatype}"
        endpoint += f"&apikey={self.api_key}"

        return call_api(endpoint)
    

    def get_monthly(self, from_symbol: str, to_symbol: str, datatype: str = 'json') -> json:
        """ 
        Returns the monthly time series (timestamp, open, high, low, close) of the FX currency pair specified, updated realtime.
        :param datatype: `json` returns the intraday time series in JSON format; `csv` returns the time series as a CSV (comma separated value) file.
        """

        if datatype not in DATA_TYPES:
            raise ValueError(f"datatype must be one of {DATA_TYPES}")
        
        endpoint = f"https://www.alphavantage.co/query?function=FX_MONTHLY&from_symbol={from_symbol}&to_symbol={to_symbol}"
        if datatype == 'csv':
            endpoint += f"&datatype={datatype}"
        endpoint += f"&apikey={self.api_key}"

        return call_api(endpoint)



    
    