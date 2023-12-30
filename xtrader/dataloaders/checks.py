import pandas as pd
from typing import List


def _check_nan(df: pd.DataFrame, columns: List[str]) -> bool:
    """ Checks if there are NaN values in the given columns of a dataframe. """
    return df.isnull().values.any()


def _check_missing_in_hourly(df: pd.DataFrame, column: str = None) -> bool:
    """ Checks if there are missing values in the given column of a dataframe. """
    if column is None:
        series = df.index
    else:
        series = df[column]
    return series.to_series().diff().dt.total_seconds().div(3600).round().eq(1).all()