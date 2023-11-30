import requests
from typing import Optional
from datetime import datetime

from xtrader.utils import call_api

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
    
    def get_news_sentiment(self, symbols:Optional[str]=None, topics:Optional[str]=None,
                            time_from:Optional[str]=None, time_to:Optional[str]=None,
                            sort:str='LATEST', limit:int=50):
        """ 
        This API returns live and historical market news & sentiment data from a large & growing selection
        of premier news outlets around the world, covering stocks, cryptocurrencies, forex, and a wide range
        of topics such as fiscal policy, mergers & acquisitions, IPOs, etc. 

        :param symbols: The stock/crypto/forex symbols of your choice. For example: tickers=IBM will filter for articles
                         that mention the IBM ticker; tickers=COIN,CRYPTO:BTC,FOREX:USD will filter for articles that
                         simultaneously mention Coinbase (COIN), Bitcoin (CRYPTO:BTC), and US Dollar (FOREX:USD) in their content.
        :param topics: The news topics of your choice. For example: topics=technology will filter for articles that write
                        about the technology sector; topics=technology,ipo will filter for articles that simultaneously
                        cover technology and IPO in their content. Below is the full list of supported topics:

                                Blockchain: blockchain
                                Earnings: earnings
                                IPO: ipo
                                Mergers & Acquisitions: mergers_and_acquisitions
                                Financial Markets: financial_markets
                                Economy - Fiscal Policy (e.g., tax reform, government spending): economy_fiscal
                                Economy - Monetary Policy (e.g., interest rates, inflation): economy_monetary
                                Economy - Macro/Overall: economy_macro
                                Energy & Transportation: energy_transportation
                                Finance: finance
                                Life Sciences: life_sciences
                                Manufacturing: manufacturing
                                Real Estate & Construction: real_estate
                                Retail & Wholesale: retail_wholesale
                                Technology: technology

        :param time_from, time_to: The time range of the news articles you are targeting, in YYYYMMDDTHHMM format.
                                 For example: time_from=20220410T0130. If time_from is specified but time_to is missing,
                                 the API will return articles published between the time_from value and the current time.
        :param sort: By default, sort=LATEST and the API will return the latest articles first. You can also set
                     sort=EARLIEST or sort=RELEVANCE based on your use case.
        :param limit: By default, limit=50 and the API will return up to 50 matching results. You can also set
                      limit=1000 to output up to 1000 results. If you are looking for an even higher output limit,
                      please contact support@alphavantage.co to have your limit boosted.
        """


        if sort not in NEWS_SENTIMENT_SORT_OPTIONS:
            raise ValueError(f"`sort` must be one of {NEWS_SENTIMENT_SORT_OPTIONS}")
        if limit > 1000:
            raise ValueError(f"`limit` must be less than 1000")
        
        endpoint = "https://www.alphavantage.co/query?function=NEWS_SENTIMENT"
        if symbols is not None:
            endpoint += f"&symbol={symbols}"
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
        
        return call_api(endpoint)