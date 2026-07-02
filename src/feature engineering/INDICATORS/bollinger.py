"""
Bollinger Bands
"""

from ta.volatility import BollingerBands


def add_bollinger(df):
    """
    Adds Bollinger Band indicators.
    """

    bb = BollingerBands(
        close=df["close"],
        window=20,
        window_dev=2
    )

    df["BB_UPPER"] = bb.bollinger_hband()
    df["BB_MIDDLE"] = bb.bollinger_mavg()
    df["BB_LOWER"] = bb.bollinger_lband()

    return df