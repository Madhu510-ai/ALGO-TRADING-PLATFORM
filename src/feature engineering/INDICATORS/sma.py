"""
Simple Moving Average (SMA)
"""

from ta.trend import SMAIndicator


def add_sma(df):
    """
    Adds SMA indicators to the dataframe.
    """

    df["SMA_20"] = SMAIndicator(
        close=df["close"],
        window=20
    ).sma_indicator()

    df["SMA_50"] = SMAIndicator(
        close=df["close"],
        window=50
    ).sma_indicator()

    return df