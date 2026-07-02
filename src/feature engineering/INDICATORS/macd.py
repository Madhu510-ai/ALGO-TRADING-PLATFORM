"""
Moving Average Convergence Divergence (MACD)
"""

from ta.trend import MACD


def add_macd(df):
    """
    Adds MACD indicators.
    """

    macd = MACD(close=df["close"])

    df["MACD_LINE"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()
    df["MACD_HIST"] = macd.macd_diff()

    return df