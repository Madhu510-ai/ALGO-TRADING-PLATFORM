"""
Average True Range (ATR)
"""

from ta.volatility import AverageTrueRange


def add_atr(df):
    """
    Adds ATR indicator.
    """

    atr = AverageTrueRange(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        window=14
    )

    df["ATR_14"] = atr.average_true_range()

    return df