import pandas as pd
from xtrader.dataloaders.checks import _check_nan, _check_missing_in_hourly

def load_prices(path: str, check_missing: bool = False) -> pd.DataFrame:
    """ Loads hourly prices from csv file and returns a dataframe with hourly, daily and monthly prices."""
    # Import csv file
    prices_hourly = pd.read_csv(path)
    # Make column names lowercase
    prices_hourly.columns = prices_hourly.columns.str.lower()
    # Set date index
    prices_hourly = prices_hourly.set_index('date', inplace=False)
    prices_hourly.index = pd.to_datetime(prices_hourly.index)

    # Check for missing values
    if check_missing:
        if _check_nan(prices_hourly, ['open', 'high', 'low', 'close', 'volume']):
            raise ValueError("Missing values (NaN) in prices_hourly")
        if not _check_missing_in_hourly(prices_hourly):
            raise ValueError("Missing values in prices_hourly")

    # Convert to numeric
    prices_hourly = prices_hourly.astype({"open": float, "high": float, "low": float,
                                          "close": float, "volume": float,
                                          "name": str, "symbol": str})

    prices_daily = prices_hourly.resample('D').last()
    prices_monthly = prices_hourly.resample('M').last()

    return {"hourly": prices_hourly, "daily": prices_daily, "monthly": prices_monthly}
