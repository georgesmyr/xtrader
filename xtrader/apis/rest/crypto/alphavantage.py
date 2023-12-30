import pandas as pd
from typing import Any

from xtrader.apis.rest.crypto.base import BaseCryptoAPI
from xtrader.apis.utils import call_api

BASE_URL = 'https://www.alphavantage.co/query?'

OUTPUT_SIZES = ['compact', 'full']
INTRADAY_INTERVALS = ['1min', '5min', '15min', '30min', '60min']


class AlphaVantageCryptoAPI(BaseCryptoAPI):

    def __init__(self, api_key):
        self.api_key = api_key
    

    def get_exchange_rate(self, from_symbol: str, to_symbol: str) -> Any:
        """ 
        This API returns the realtime exchange rate for any pair of digital currency
        (e.g., Bitcoin) or physical currency (e.g., USD).
        """
        params = {'function': 'CURRENCY_EXCHANGE_RATE', 'from_currency': from_symbol, 'to_currency': to_symbol, 'apikey': self.api_key}
        return call_api(base_url=BASE_URL, params=params)
    

    def get_intraday(self, symbol: str, market: str, interval: str, outputsize: str='compact') -> Any:
        """
        Returns intraday time series (timestamp, open, high, low, close, volume)
        of the cryptocurrency specified, updated realtime.

        :param outputsize: `compact` returns only the latest 100 data points in the intraday time series;`full` returns the full-length intraday time series. 
                           The `compact` option is recommended if you would like to reduce the data size of each API call.
        """
        if outputsize not in OUTPUT_SIZES:
            raise ValueError(f'`outputsize` must be one of: {outputsize}')
        if interval not in INTRADAY_INTERVALS:
            raise ValueError(f'`interval` must be one of: {interval}')
        
        params = {'function': 'CRYPTO_INTRADAY', 'symbol': symbol, 'market': market, 'interval': interval,
                  'outputsize': outputsize, 'apikey': self.api_key}
        return call_api(base_url=BASE_URL, params=params)
    

    def get_daily(self, symbol: str, market: str) -> Any:
        """ 
        Returns the daily historical time series for a digital currency
        (e.g., BTC) traded on a specific market (e.g., CNY/Chinese Yuan), refreshed daily at midnight (UTC).
        Prices and volumes are quoted in both the market-specific currency and USD.
        """
        params = {'function': 'DIGITAL_CURRENCY_DAILY', 'symbol': symbol, 'market': market, 'apikey': self.api_key}
        return call_api(base_url=BASE_URL, params=params)
    
    
    def get_weekly(self, symbol: str, market: str) -> Any:
        """ 
        Returns the weekly historical time series for a digital currency
        (e.g., BTC) traded on a specific market (e.g., CNY/Chinese Yuan), refreshed daily at midnight (UTC).
        Prices and volumes are quoted in both the market-specific currency and USD.
        """
        params = {'function': 'DIGITAL_CURRENCY_WEEKLY', 'symbol': symbol, 'market': market, 'apikey': self.api_key}
        return call_api(base_url=BASE_URL, params=params)
    

    def get_monthly(self, symbol: str, market: str) -> Any:
        """ 
        Returns the monthly historical time series for a digital currency
        (e.g., BTC) traded on a specific market (e.g., CNY/Chinese Yuan), refreshed daily at midnight (UTC).
        Prices and volumes are quoted in both the market-specific currency and USD.
        """
        params = {'function': 'DIGITAL_CURRENCY_MONTHLY', 'symbol': symbol, 'market': market, 'apikey': self.api_key}
        return call_api(base_url=BASE_URL, params=params)