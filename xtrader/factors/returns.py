import pandas as pd

from typing import Optional
from typing import List
from typing import Union

from xtrader.factors import utils
from xtrader.utils import TIME_SYMBOLS


class Returns(object):

    def __init__(self, prices: Optional[pd.DataFrame] = None):
        """ Initializes the `Returns` class."""
        self.prices = prices.copy()

    def from_defaults(self):
        pass

    @staticmethod
    def returns(prices: pd.DataFrame, periods: List[int], freq: str, columns: Optional[Union[str, List[str]]] = None,
                normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
        """ 
        Calculates lagged returns from prices. The returns are optionally normalized with the geometric average.
        
        :param prices: Prices to calculate the returns from.
        :param periods: List of periods to calculate the returns for.
        :param freq: Frequency of the prices. Can be 'h' for hour, 'd' for day etc.
        :param columns: List of columns to calculate the returns for. If None, the returns are calculated for all columns.
        :param normalize: If True, the returns are normalized with the geometric average.
        :param dropna: If True, the rows with NaNs are dropped.
        :param return_full: If True, the full dataframe is returned. If False, only the columns with the returns are returned.
        """
        prices = prices.copy()
        # Set Columns to calculate the lagged returns for
        columns = utils._get_columns(columns, ['high', 'low', 'open', 'close', 'volume'])

        # For each column calculate the lagged returns for the lags that were specified
        for column in columns:
            for period in periods:
                prices[f'{column}_return_{period}{freq}'] = prices[column].pct_change(period)
                # Normalize returns
                if normalize:
                    prices[f'{column}_return_{period}{freq}'] = prices[f'{column}_return_{period}{freq}'].add(1).pow(1 / period).sub(1)

        # Drop NaNs
        if dropna:
            prices.dropna(inplace=True)
        # Return full dataframe or only the columns with the returns
        if not return_full:
            return prices[[f'{column}_return_{period}{freq}' for column in columns for period in periods]]
        
        return prices

    @staticmethod
    def hourly(prices: pd.DataFrame, periods: List[int], columns: Optional[List[str]] = None,
               normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
        """ Calculates hourly lagged returns from hourly prices."""
        return Returns.returns(prices, periods, TIME_SYMBOLS["hour"], columns, normalize, dropna, return_full)

    @staticmethod
    def daily(prices: pd.DataFrame, periods: List[int], columns: Optional[List[str]] = None,
             normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
        """ Calculates daily lagged returns from daily prices."""
        return Returns.returns(prices, periods, TIME_SYMBOLS["day"], columns, normalize, dropna, return_full)

    @staticmethod
    def monthly(prices: pd.DataFrame, periods: List[int], columns: Optional[List[str]] = None,
                normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
        """ Calculates monthly lagged returns from monthly prices."""
        return Returns.returns(prices, periods, TIME_SYMBOLS["month"], columns, normalize, dropna, return_full)

    @staticmethod
    def lagged_returns(prices: pd.DataFrame, lags: List[int], freq: str, columns: Optional[Union[str, List[str]]] = None,
                       normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
        """ 
        Calculates lagged returns from prices. The returns are optionally normalized with the geometric average.

        :param prices: Prices to calculate the returns from.
        :param lags: List of lags to calculate the returns for.
        :param freq: Frequency of the prices label. Can be 'h' for hour, 'd' for day etc.
        :param columns: List of columns to calculate the returns for. If None, the returns are calculated for all columns.
        :param normalize: If True, the returns are normalized with the geometric average.
        :param dropna: If True, the rows with NaNs are dropped.
        :param return_full: If True, the full dataframe is returned. If False, only the columns with the returns are returned.
        """
        prices = prices.copy()
        # Set Columns to calculate the lagged returns for
        columns = utils._get_columns(columns, ['high', 'low', 'open', 'close', 'volume'])

        # For each column calculate the lagged returns for the lags that were specified
        for column in columns:
            if f"{column}_return_1{freq}" not in prices.columns:
                prices[f'{column}_return_1{freq}'] = Returns.returns(prices, [1], freq,
                                                                            [column], normalize, dropna, False)[f'{column}_return_1{freq}']
            for lag in lags:
                prices[f'{column}_return_1{freq}_lag_{lag}'] = prices[f'{column}_return_1{freq}'].shift(lag)

        # Drop NaNs
        if dropna:
            prices.dropna(inplace=True)
        # Return full dataframe or only the columns with the returns
        if not return_full:
            return prices[[f'{column}_return_1{freq}_lag_{lag}' for column in columns for lag in lags]]
        
        return prices

    @staticmethod
    def hourly_lagged(prices: pd.DataFrame, lags: List[int], columns: Optional[List[str]] = None,
                      normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
        """ Calculates hourly lagged returns from hourly prices."""
        return Returns.lagged_returns(prices, lags, TIME_SYMBOLS["hour"], columns, normalize, dropna, return_full)

    @staticmethod
    def daily_lagged(prices: pd.DataFrame, lags: List[int], columns: Optional[List[str]] = None,
                     normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
        """ Calculates daily lagged returns from daily prices."""
        return Returns.lagged_returns(prices, lags, TIME_SYMBOLS["day"], columns, normalize, dropna, return_full)

    @staticmethod
    def monthly_lagged(prices: pd.DataFrame, lags: List[int], columns: Optional[List[str]] = None,
                       normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
        """ Calculates monthly lagged returns from monthly prices."""
        return Returns.lagged_returns(prices, lags, TIME_SYMBOLS["month"], columns, normalize, dropna, return_full)

    @staticmethod
    def forward_returns(prices: pd.DataFrame, lags: List[int],  freq: str, columns: Optional[Union[str, List[str]]] = None,
                        normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
        """ 
        Calculates forward returns from prices. The returns are optionally normalized with the geometric average.
        
        :param prices: Prices to calculate the returns from.
        :param lags: List of lags to calculate the returns for.
        :param freq: Frequency of the prices label. Can be 'h' for hour, 'd' for day etc.
        :param columns: List of columns to calculate the returns for. If None, the returns are calculated for all columns.
        :param normalize: If True, the returns are normalized with the geometric average.
        :param dropna: If True, the rows with NaNs are dropped.
        :param return_full: If True, the full dataframe is returned. If False, only the columns with the returns are returned.
        """
        prices = prices.copy()
        # Set Columns to calculate the lagged returns for
        columns = utils._get_columns(columns, ['high', 'low', 'open', 'close', 'volume'])

        # For each column calculate the lagged returns for the lags that were specified
        for column in columns:
            for lag in lags:
                if f"{column}_return_{lag}{freq}" not in prices.columns:
                    prices[f'{column}_return_{lag}{freq}'] = Returns.returns(prices, [lag], freq, [column], normalize, dropna, False)[f'{column}_return_{lag}{freq}']
            
            for lag in lags:
                prices[f"{column}_target_{lag}{freq}"] = prices[f"{column}_return_{lag}{freq}"].shift(-lag)

        # Drop NaNs
        if dropna:
            prices.dropna(inplace=True)
        # Return full dataframe or only the columns with the returns
        if not return_full:
            return prices[[f'{column}_target_{lag}{freq}' for column in columns for lag in lags]]
        
        return prices

    @staticmethod
    def hourly_forward(prices: pd.DataFrame, lags: List[int], columns: Optional[List[str]] = None,
                       normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
        """ Calculates hourly forward returns from hourly prices."""
        return Returns.forward_returns(prices, lags, TIME_SYMBOLS["hour"], columns, normalize, dropna, return_full)

    @staticmethod
    def daily_forward(prices: pd.DataFrame, lags: List[int], columns: Optional[List[str]] = None,
                      normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
        """ Calculates daily forward returns from daily prices."""
        return Returns.forward_returns(prices, lags, TIME_SYMBOLS["day"], columns, normalize, dropna, return_full)

    @staticmethod
    def monthly_forward(prices: pd.DataFrame, lags: List[int], columns: Optional[List[str]] = None,
                        normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
        """ Calculates monthly forward returns from monthly prices."""
        return Returns.forward_returns(prices, lags, TIME_SYMBOLS["month"], columns, normalize, dropna, return_full)
    