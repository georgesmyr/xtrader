import pandas as pd
from typing import Optional, List

from xtrader.factors import utils
from xtrader.utils import TIME_SYMBOLS



def get_returns(prices: pd.DataFrame, periods: List[int], freq: str, columns: Optional[List[str]] = None,
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


def get_hourly_returns(prices: pd.DataFrame, periods: List[int], columns: Optional[List[str]] = None,
                       normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
    """ Calculates hourly lagged returns from hourly prices."""
    return get_returns(prices, periods, TIME_SYMBOLS["hour"], columns, normalize, dropna, return_full)


def get_daily_returns(prices: pd.DataFrame, periods: List[int], columns: Optional[List[str]] = None,
                      normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
    """ Calculates daily lagged returns from daily prices."""
    return get_returns(prices, periods, TIME_SYMBOLS["day"], columns, normalize, dropna, return_full)


def get_monthly_returns(prices: pd.DataFrame, periods: List[int], columns: Optional[List[str]] = None,
                        normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
    """ Calculates monthly lagged returns from monthly prices."""
    return get_returns(prices, periods, TIME_SYMBOLS["month"], columns, normalize, dropna, return_full)




def get_lagged_returns(prices: pd.DataFrame, lags: List[int], freq: str, columns: Optional[List[str]] = None, from_period: int = 1,
                       normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
    """ 
    Calculates lagged returns from prices. The returns are optionally normalized with the geometric average.

    :param prices: Prices to calculate the returns from.
    :param lags: List of lags to calculate the returns for.
    :param freq: Frequency of the prices label. Can be 'h' for hour, 'd' for day etc.
    :param columns: List of columns to calculate the returns for. If None, the returns are calculated for all columns.
    :param from_period: Period to calculate the returns from.
    :param normalize: If True, the returns are normalized with the geometric average.
    :param dropna: If True, the rows with NaNs are dropped.
    :param return_full: If True, the full dataframe is returned. If False, only the columns with the returns are returned.
    """
    prices = prices.copy()
    # Set Columns to calculate the lagged returns for
    columns = utils._get_columns(columns, ['high', 'low', 'open', 'close', 'volume'])

    # For each column calculate the lagged returns for the lags that were specified
    for column in columns:
        if f"{column}_return_{from_period}{freq}" not in prices.columns:
            prices[f'{column}_return_{from_period}{freq}'] = get_returns(prices, [from_period], freq,
                                                                         [column], normalize, dropna, False)[f'{column}_return_{from_period}{freq}']
        for lag in lags:
            prices[f'{column}_return_{from_period}{freq}_lag_{lag}'] = prices[f'{column}_return_{from_period}{freq}'].shift(lag)

    # Drop NaNs
    if dropna:
        prices.dropna(inplace=True)
    # Return full dataframe or only the columns with the returns
    if not return_full:
        return prices[[f'{column}_return_{from_period}{freq}_lag_{lag}' for column in columns for lag in lags]]
    
    return prices


def get_hourly_lagged_returns(prices: pd.DataFrame, lags: List[int], columns: Optional[List[str]] = None, from_period: int = 1,
                              normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
    """ Calculates hourly lagged returns from hourly prices."""
    return get_lagged_returns(prices, from_period, lags, TIME_SYMBOLS["hour"], columns, normalize, dropna, return_full)


def get_daily_lagged_returns(prices: pd.DataFrame, lags: List[int], columns: Optional[List[str]] = None, from_period: int = 1,
                             normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
    """ Calculates daily lagged returns from daily prices."""
    return get_lagged_returns(prices, from_period, lags, TIME_SYMBOLS["day"], columns, normalize, dropna, return_full)


def get_monthly_lagged_returns(prices: pd.DataFrame, lags: List[int], columns: Optional[List[str]] = None,  from_period: int = 1,
                               normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
    """ Calculates monthly lagged returns from monthly prices."""
    return get_lagged_returns(prices, from_period, lags, TIME_SYMBOLS["month"], columns, normalize, dropna, return_full)




def get_forward_returns(prices: pd.DataFrame, lags: List[int],  freq: str, columns: Optional[List[str]] = None,
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
                prices[f'{column}_return_{lag}{freq}'] = get_returns(prices, [lag], freq, [column], normalize, dropna, False)[f'{column}_return_{lag}{freq}']
        
        for lag in lags:
            prices[f"{column}_target_{lag}{freq}"] = prices[f"{column}_return_{lag}{freq}"].shift(-lag)

    # Drop NaNs
    if dropna:
        prices.dropna(inplace=True)
    # Return full dataframe or only the columns with the returns
    if not return_full:
        return prices[[f'{column}_return_{freq}_forward_{lag}' for column in columns for lag in lags]]
    
    return prices


def get_hourly_forward_returns(prices: pd.DataFrame, lags: List[int], columns: Optional[List[str]] = None,
                               normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
    """ Calculates hourly forward returns from hourly prices."""
    return get_forward_returns(prices, lags, TIME_SYMBOLS["hour"], columns, normalize, dropna, return_full)


def get_daily_forward_returns(prices: pd.DataFrame, lags: List[int], columns: Optional[List[str]] = None,
                              normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
    """ Calculates daily forward returns from daily prices."""
    return get_forward_returns(prices, lags, TIME_SYMBOLS["day"], columns, normalize, dropna, return_full)


def get_monthly_forward_returns(prices: pd.DataFrame, lags: List[int], columns: Optional[List[str]] = None,
                                normalize: bool = True, dropna: bool = False, return_full: bool = True) -> pd.DataFrame:
    """ Calculates monthly forward returns from monthly prices."""
    return get_forward_returns(prices, lags, TIME_SYMBOLS["month"], columns, normalize, dropna, return_full)

