from talib import RSI
from talib import BBANDS

import pandas as pd

from typing import Optional
from typing import Union
from typing import List

from xtrader.factors import utils


class TechnicalFactors(object):


    def __init__(self, prices: Optional[pd.DataFrame] = None):
        """ Initializes the `TechnicalFactors` class."""
        self.prices = prices

    @staticmethod
    def bbands(prices: pd.DataFrame, time_period: int = 21, stds_up: int = 2, stds_down: int = 2, freq: str = '', 
               columns: Optional[Union[str, List[str]]] = None, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
        """ 
        Bollinger Bands consist of a simple moving average (SMA) surrounded by bands two rolling
        standard deviations below and above the SMA. It was introduced for the visualization of
        potential overbought/oversold conditions when the price dipped outside the two bands on
        the upper or lower side, respectively.

        :param prices: prices dataframe
        :param time_period: period for RSI
        :parram stds_up: number of standard deviations for upper band
        :parram stds_down: number of standard deviations for lower band
        :param columns: columns to calculate BBANDS for
        :param dropna: drop NaNs
        :param return_full: return full dataframe or only BBANDS columns
        """
        prices = prices.copy()
        # Set the columns to calculate BBANDS for
        columns = utils._get_columns(columns, ['open', 'high', 'low', 'close', 'volume'])

        for column in columns:
            up, mid, low = BBANDS(prices['close'], timeperiod=time_period, nbdevup=stds_up, nbdevdn=stds_down)
            prices[f'{column}_bbands_{time_period}{freq}_{stds_up}_{stds_down}_up'] = up
            prices[f'{column}_bbands_{time_period}{freq}_{stds_up}_{stds_down}_mid'] = mid
            prices[f'{column}_bbands_{time_period}{freq}_{stds_up}_{stds_down}_low'] = low

        # Drop NaNs
        if dropna:
            prices.dropna(inplace=True)

        if not return_full:
            cols = [f'{column}_bbands_{time_period}{freq}_{stds_up}_{stds_down}_{x}' 
                    for column in columns for x in ['up', 'mid', 'low']]
            return prices[cols]
        
        return prices
    
    @staticmethod
    def rsi(prices: pd.DataFrame, time_period: int = 21, freq: str = '',
            columns: Optional[Union[str, List[str]]] = None, dropna: bool = False,
            return_full: bool = True) -> pd.DataFrame:
        """ 
        RSI (Relative strencth Index) compares the magnitude of recent price changes
        across stocks to identify stocks as overbought or oversold. A high RSI (usually above 70)
        indicates overbought and a low RSI (typically below 30) indicates oversold.

        :param prices: prices dataframe
        :param time_period: period for RSI
        """
        prices = prices.copy()

        # Set the columns to calculate RSI for
        columns = utils._get_columns(columns, ['open', 'high', 'low', 'close', 'volume'])

        for column in columns:
            prices[f'{column}_rsi_{time_period}{freq}'] = RSI(prices['close'], timeperiod=time_period)

        # Drop NaNs
        if dropna:
            prices.dropna(inplace=True)
        
        if not return_full:
            cols = [f'{column}_rsi_{time_period}{freq}' for column in columns]
            return prices[cols]
        
        return prices

