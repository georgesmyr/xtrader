import pandas as pd
from typing import List


def get_lagged_returns(prices: pd.DataFrame, lags: List[int], freq: str):
    """ Calculates lagged returns from prices."""
    for lag in lags:
        prices[f'high_return_{lag}{freq}'] = prices['high'].pct_change(lag)
        prices[f'low_return_{lag}{freq}'] = prices['low'].pct_change(lag)
        prices[f'open_return_{lag}{freq}'] = prices['open'].pct_change(lag)
        prices[f'close_return_{lag}{freq}'] = prices['close'].pct_change(lag)
        prices[f'volume_return_{lag}{freq}'] = prices['volume'].pct_change(lag)
    return prices


def get_hourly_returns(prices: pd.DataFrame, lags: List[int]):
    """ Calculates hourly lagged returns from hourly prices."""
    return get_lagged_returns(prices, lags, 'h')


def get_daily_returns(prices: pd.DataFrame, lags: List[int]):
    """ Calculates daily lagged returns from daily prices."""
    return get_lagged_returns(prices, lags, 'd')


def get_monthly_returns(prices: pd.DataFrame, lags: List[int]):
    """ Calculates monthly lagged returns from monthly prices."""
    return get_lagged_returns(prices, lags, 'm')