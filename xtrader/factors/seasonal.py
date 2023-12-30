import pandas as pd
from typing import Optional


class SeasonalFactors(object):

    def __init__(self, prices: Optional[pd.DataFrame] = None):
        """ Initializes the `Seasonal` factors class."""
        self.prices = prices.copy()

    @staticmethod
    def time_indicators(prices: pd.DataFrame, return_full: bool = True):
        """ 
        Gets time indicators like month, day of week, etc. 
        :param prices: prices dataframe
        :param return_full: return full dataframe or just the indicators
        """
        prices = prices.copy()
        prices['day'] = prices.index.day
        prices['day_of_week'] = prices.index.dayofweek
        prices['week_of_year'] = prices.index.isocalendar().week  
        prices['month'] = prices.index.month  
        prices['quarter'] = prices.index.quarter
        prices['year'] = prices.index.year
        
        if return_full:
            return prices
        else:
            return prices[['month', 'day', 'day_of_week', 'week_of_year', 'quarter', 'year']]