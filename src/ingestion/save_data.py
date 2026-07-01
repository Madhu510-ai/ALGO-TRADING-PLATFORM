from pathlib import Path
from datetime import datetime

import pandas as pd

from .config import RAW_DATA_PATH


def save_to_csv(
    dataframe: pd.DataFrame,
    ticker: str
) -> Path:
    """
    Save a dataframe into a date-wise folder.

    Example

    data/raw/
        2026-07-01/
            RELIANCE.csv
            TCS.csv
    """

    # Today's folder
    today = datetime.now().strftime("%Y-%m-%d")

    save_directory = RAW_DATA_PATH / today

    save_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = save_directory / f"{ticker}.csv"

    dataframe.to_csv(
        file_path,
        index=False
    )

    return file_path