"""
Relative Strength Index (RSI)
"""

from ta.momentum import RSIIndicator


def add_rsi(df):
    """
    Adds RSI indicator.
    """

    df["RSI_14"] = RSIIndicator(
        close=df["close"],
        window=14
    ).rsi()

    return df