"""
Exponential Moving Average (EMA)
"""

from ta.trend import EMAIndicator


def add_ema(df):
    """
    Adds EMA indicators to the dataframe.
    """

    df["EMA_20"] = EMAIndicator(
        close=df["close"],
        window=20
    ).ema_indicator()

    df["EMA_50"] = EMAIndicator(
        close=df["close"],
        window=50
    ).ema_indicator()

    return df