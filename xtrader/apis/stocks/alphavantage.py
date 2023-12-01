import requests
from typing import Any, Optional

from xtrader.utils import call_api
from xtrader.apis.format import AV_OHLC_response_format
from xtrader.apis.stocks.base import BaseStockAPI

BASE_URL = 'https://www.alphavantage.co/query?'
OUTPUT_SIZES = ['compact', 'full']
INTRADAY_INTERVALS = ['1min', '5min', '15min', '30min', '60min']

class AlphaVantageStockAPI(BaseStockAPI):  

    def __init__(self, api_key):
        """ Initialize the API object with AlphaVantage API key."""
        self.api_key = api_key


    def get_daily(self, symbol, adjusted: bool = False, outputsize: str = 'compact') -> Any:
        """ 
        Get daily stock data for a given symbol.
        
        :param outputsize: By default, outputsize=compact. Strings compact and full are accepted with the following
                            specifications: compact returns only the latest 100 data points; full returns the full-length
                            time series of 20+ years of historical data. The "compact" option is recommended if you would 
                            like to reduce the data size of each API call.
        """
        if outputsize not in OUTPUT_SIZES:
            raise ValueError(f'`outputsize` must be one of {OUTPUT_SIZES}')
        
        if adjusted:
            function = 'TIME_SERIES_DAILY_ADJUSTED'
        else:
            function = 'TIME_SERIES_DAILY'
        params = {'function': function, 'symbol': symbol, 'apikey': self.api_key}
        response = call_api(base_url=BASE_URL, params=params).json()
        
        return AV_OHLC_response_format(response, 'Time Series (Daily)')


    def get_intraday(self, symbol: str, interval: str = '5min', adjusted: bool = True, 
                     extended_hours: bool = True, month:Optional[str]=None, outputsize='compact') -> Any:
        """ 
        Get intraday stock data for a given symbol.
        
        :param outputsize: By default, outputsize=compact. Strings compact and full are accepted with the following
                            specifications: compact returns only the latest 100 data points; full returns the full-length
                            time series of 20+ years of historical data. The "compact" option is recommended if you would 
                            like to reduce the data size of each API call.
        """
        if outputsize not in OUTPUT_SIZES:
            raise ValueError(f'`outputsize` must be one of {OUTPUT_SIZES}')
        if interval not in INTRADAY_INTERVALS:
            raise ValueError(f'`interval` must be one of {INTRADAY_INTERVALS}')
        
        params = {'function': 'TIME_SERIES_INTRADAY', 'symbol': symbol, 'interval': interval, 'month': month,
                  'adjusted': adjusted, 'extended_hours': extended_hours, 'outputsize': outputsize, 'apikey': self.api_key}
        response = call_api(base_url=BASE_URL, params=params).json()
        
        return AV_OHLC_response_format(response, f'Time Series ({interval})')  


    def get_weekly(self, symbol: str, adjusted: bool = False) -> Any:
        """ 
        Get weekly stock data for a given symbol.

        :param outputsize: By default, outputsize=compact. Strings compact and full are accepted with the following
                            specifications: compact returns only the latest 100 data points; full returns the full-length
                            time series of 20+ years of historical data. The "compact" option is recommended if you would 
                            like to reduce the data size of each API call.
        """
        if adjusted:
            function = 'TIME_SERIES_WEEKLY_ADJUSTED'
        else:
            function = 'TIME_SERIES_WEEKLY'
        params = {'function': function, 'symbol': symbol, 'apikey': self.api_key}
        response = call_api(base_url=BASE_URL, params=params).json()

        return AV_OHLC_response_format(response, 'Weekly Time Series')
    

    def get_monthly(self, symbol: str, adjusted: bool = False):
        """ Get monthly stock data for a given symbol. """
        if adjusted:
            function = 'TIME_SERIES_MONTHLY_ADJUSTED'
        else:
            function = 'TIME_SERIES_MONTHLY'
        params = {'function': function, 'symbol': symbol, 'apikey': self.api_key}
        response = call_api(base_url=BASE_URL, params=params).json()

        return AV_OHLC_response_format(response, 'Monthly Time Series')

    

    def search_symbol(self, keywords):
        """ Search for a symbol based on keywords. """""
        params = {'function': 'SYMBOL_SEARCH', 'keywords': keywords, 'apikey': self.api_key}
        return call_api(base_url=BASE_URL, params=params)
    
    def global_market_status(self):
        """ Get the current global market status. """
        params = {'function': 'MARKET_STATUS', 'apikey': self.api_key}  
        return call_api(base_url=BASE_URL, params=params)


    