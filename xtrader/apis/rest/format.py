import pandas as pd
from typing import Any

def AV_OHLC_response_format(response: Any, data_key: str) -> pd.DataFrame:
    """ 
    Receives the AlphaVantage response, handles errors
    and returns a DataFrame with OHLC format
    """
    if 'Information' in response.keys():
        raise ValueError(response['Information'])
    elif 'Error Message' in response.keys():
        raise ValueError(response['Error Message'])
    
    data = response[data_key]
    dates = list(data.keys())
    data_df = pd.DataFrame({'date': dates,
                                'open': [data[date]['1. open'] for date in dates],
                                'high': [data[date]['2. high'] for date in dates],
                                'low': [data[date]['3. low'] for date in dates],
                                'close': [data[date]['4. close'] for date in dates],
                                'volume': [data[date]['5. volume'] for date in dates]})
    return data_df