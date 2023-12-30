from typing import List, Optional

def _get_columns(columns: Optional[List[str]], default: List[str]) -> List[str]:
    """ Returns the columns to calculate the lagged returns for """
    if columns is None:
        return default
    else:
        if isinstance(columns, str):
            columns = [columns]
        return [col.lower() for col in columns]
    