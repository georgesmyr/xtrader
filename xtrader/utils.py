import pandas as pd

TIME_SYMBOLS = {"hour": "h", "day": "d", "month": "m"}

def select_columns(df: pd.DataFrame, name: str, drop_name: bool = False):
    """Selects columns from a dataframe"""
    # Select columns that start with name
    df_selected = df[[column for column in df.columns if column.startswith(name)]]
    
    # Drop name from column names
    if drop_name:
        df_selected.columns = [column[len(name) + 1:] for column in df_selected.columns]

    return df_selected

