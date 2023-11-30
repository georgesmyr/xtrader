import requests
from typing import Optional

from datetime import datetime

NEWS_SENTIMENT_SORT_OPTIONS = ['LATEST', 'RELEVANCE']

def is_valid_time_format(input_string):
    try:
        datetime.strptime(input_string, '%Y%m%dT%H%M')
        return True
    except ValueError:
        return False

class AlphaVantageNewsSentimentAPI:

    def __init__(self, api_key):
        self.api_key = api_key


    def call_api(self, endpoint):
        response = requests.get(endpoint)
        if response.status_code != 200:
            raise ValueError(f'Invalid API response: {response}')
        return response

    
    def get_news_sentiment(self, symbol:Optional[str]=None, topics:Optional[str]=None,
                            time_from:Optional[str]=None, time_to:Optional[str]=None,
                            sort:str='LATEST', limit:int=50):
        """ 
        This API returns live and historical market news & sentiment data from a large & growing selection
        of premier news outlets around the world, covering stocks, cryptocurrencies, forex, and a wide range
        of topics such as fiscal policy, mergers & acquisitions, IPOs, etc. 
        """


        if sort not in NEWS_SENTIMENT_SORT_OPTIONS:
            raise ValueError(f"`sort` must be one of {NEWS_SENTIMENT_SORT_OPTIONS}")
        if limit > 1000:
            raise ValueError(f"`limit` must be less than 1000")
        
        endpoint = "https://www.alphavantage.co/query?function=NEWS_SENTIMENT"
        if symbol is not None:
            endpoint += f"&symbol={symbol}"
        if topics is not None:
            endpoint += f"&topics={topics}"
        if time_from is not None:
            if not is_valid_time_format(time_from):
                raise ValueError(f"`time_from` must be in the format YYYYMMDDTHHMM")
            endpoint += f"&time_from={time_from}"
            if time_to is not None:
                if not is_valid_time_format(time_to):
                    raise ValueError(f"`time_to` must be in the format YYYYMMDDTHHMM")
                endpoint += f"&time_to={time_to}"
        if sort == 'RELEVANCE':
            endpoint += f"&sort=RELEVANCE"
        endpoint += f"&apikey={self.api_key}"
        
        return self.call_api(endpoint)