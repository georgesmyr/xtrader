import requests
from xtrader.utils import call_api
from xtrader.apis.stocks.base import BaseStockAPI

OUTPUT_SIZES = ['compact', 'full']
DATA_TYPES = ['json', 'csv']
INTRADAY_INTERVALS = ['1min', '5min', '15min', '30min', '60min']

class AlphaVantageStockAPI(BaseStockAPI):  

    def __init__(self, api_key):
        self.api_key = api_key


    def get_daily(self, symbol, adjusted=False, outputsize='compact', datatype='json'):
        """ Get daily stock data for a given symbol. """
        if outputsize not in OUTPUT_SIZES:
            raise ValueError(f'`outputsize` must be one of {OUTPUT_SIZES}')
        if datatype not in DATA_TYPES:
            raise ValueError(f'`datatype` must be one of {DATA_TYPES}')
        
        if adjusted:
            function = 'TIME_SERIES_DAILY_ADJUSTED'
        else:
            function = 'TIME_SERIES_DAILY'

        endpoint = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}'
        if outputsize == 'full':
            endpoint += '&outputsize=full'
        if datatype == 'csv':
            endpoint += '&datatype=csv'
        endpoint += f'&apikey={self.api_key}'

        return call_api(endpoint)
    

    def get_intraday(self, symbol, interval='5min', adjusted=True, extended_hours=True,
                    month=None, outputsize='compact', datatype='json'):
        """ Get intraday stock data for a given symbol."""
        if outputsize not in OUTPUT_SIZES:
            raise ValueError(f'`outputsize` must be one of {OUTPUT_SIZES}')
        if datatype not in DATA_TYPES:
            raise ValueError(f'`datatype` must be one of {DATA_TYPES}')
        if interval not in INTRADAY_INTERVALS:
            raise ValueError(f'`interval` must be one of {INTRADAY_INTERVALS}')
        
        endpoint = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}'
        if month is not None:
            endpoint += f'&month={month}'
        if not adjusted:
            endpoint += '&adjusted=false'
        if not extended_hours:
            endpoint += '&extended_hours=false'
        if outputsize == 'full':
            endpoint += '&outputsize=full'
        if datatype == 'csv':
            endpoint += '&datatype=csv'
        endpoint += f'&apikey={self.api_key}'
        
        return call_api(endpoint)       


    def get_weekly(self, symbol, adjusted=False, datatype='json'):
        """ Get weekly stock data for a given symbol."""
        if datatype not in DATA_TYPES:
            raise ValueError(f'datatype must be one of {DATA_TYPES}')
        if adjusted:
            function = 'TIME_SERIES_WEEKLY_ADJUSTED'
        else:
            function = 'TIME_SERIES_WEEKLY'

        endpoint = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}'
        if datatype == 'csv':
            endpoint += '&datatype=csv'
        endpoint += f'&apikey={self.api_key}'

        return call_api(endpoint)
    

    def get_monthly(self, symbol, adjusted=False, datatype='json'):
        """ Get monthly stock data for a given symbol."""
        if datatype not in DATA_TYPES:
            raise ValueError(f'datatype must be one of {DATA_TYPES}')
        if adjusted:
            function = 'TIME_SERIES_MONTHLY_ADJUSTED'
        else:
            function = 'TIME_SERIES_MONTHLY'

        endpoint = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}'
        if datatype == 'csv':
            endpoint += '&datatype=csv'
        endpoint += f'&apikey={self.api_key}'

        return call_api(endpoint)
    

    def search_symbol(self, keywords, datatype='json'):
        """ Search for a symbol based on keywords. """""
        if datatype not in DATA_TYPES:
            raise ValueError(f'datatype must be one of {DATA_TYPES}')
        
        endpoint = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keywords}'
        if datatype == 'csv':
            endpoint += '&datatype=csv'
        endpoint += f'&apikey={self.api_key}'

        return call_api(endpoint)
    
    def global_market_status(self):
        """ Get the current global market status. """
        endpoint = f'https://www.alphavantage.co/query?function=MARKET_STATUS&apikey={self.api_key}'
        
        return call_api(endpoint)


    