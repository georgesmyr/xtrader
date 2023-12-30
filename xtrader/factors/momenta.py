import pandas as pd

from typing import Optional
from typing import List
from typing import Union

from xtrader.factors.returns import ReturnFactors
from xtrader.factors import utils
from xtrader.utils import TIME_SYMBOLS


class MomentumFactors(object):

    def __init__(self, prices: Optional[pd.DataFrame]):
        """ Initializes the `MomentumFactors` class."""
        self.prices = prices

    @staticmethod
    def momenta(prices: pd.DataFrame, periods: List[int], freq: str, columns: Optional[Union[List[str], str]] = None,
                    normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
        """ Calculates momentums from prices."""
        prices = prices.copy()
        # Set Columns to calculate the lagged momentums for
        columns = utils._get_columns(columns, ['high', 'low', 'open', 'close', 'volume'])

        # If period 1 is in periods, raise value error
        if 1 in periods:
            raise ValueError("Period 1 is not allowed for momenta")
        
        for column in columns:
            # If return_1 is not in prices, calculate it
            if not f"{column}_return_1{freq}" in prices.columns:
                prices[f"{column}_return_1{freq}"] = ReturnFactors.returns(prices, [1], freq, [column], normalize, dropna, return_full=False)[f"{column}_return_1{freq}"]
            
            for period in periods:
                if not f"column_return_{period}{freq}" in prices.columns:
                    prices[f"{column}_return_{period}{freq}"] = ReturnFactors.returns(prices, [period], freq, [column],
                                                                            normalize, dropna, return_full=False)[f"{column}_return_{period}{freq}"]

                prices[f"{column}_momentum_{period}{freq}"] = prices[f"{column}_return_{period}{freq}"].sub(prices[f"{column}_return_1{freq}"])

            # Calculate momentum 3-12
            if (3 in periods) and (12 in periods):
                print(True)
                prices[f"{column}_momentum_3_12{freq}"] = prices[f"{column}_momentum_12{freq}"].sub(prices[f"{column}_momentum_3{freq}"])
        
        # Drop NaNs
        if dropna:
            prices.dropna(inplace=True)

        # Return full dataframe or only the columns with the momenta
        if not return_full:
            cols = [f'{column}_momentum_{period}{freq}' for column in columns for period in periods]
            if (3 in periods) and (12 in periods):
                cols += [f'{column}_momentum_3_12{freq}' for column in columns]
            return prices[cols]
            
        return prices

    @staticmethod
    def hourly(prices: pd.DataFrame, periods: List[int], columns: Optional[List[str]] = None,
               normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
        """ Calculates hourly momenta from hourly prices."""
        return MomentumFactors.momenta(prices, periods, TIME_SYMBOLS["hour"], columns, normalize, dropna, return_full)

    @staticmethod
    def daily(prices: pd.DataFrame, periods: List[int], columns: Optional[List[str]] = None,
              normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
        """ Calculates daily momenta from daily prices."""
        return MomentumFactors.momenta(prices, periods, TIME_SYMBOLS["day"], columns, normalize, dropna, return_full)

    @staticmethod
    def monthly(prices: pd.DataFrame, periods: List[int], columns: Optional[List[str]] = None,
                normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
        """ Calculates monthly momenta from monthly prices."""
        return MomentumFactors.momenta(prices, periods, TIME_SYMBOLS["month"], columns, normalize, dropna, return_full)