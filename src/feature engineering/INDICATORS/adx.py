"""
Average Directional Index (ADX)
"""

from ta.trend import ADXIndicator


def add_adx(df):
    """
    Adds ADX indicator.
    """

    adx = ADXIndicator(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        window=14
    )

    df["ADX_14"] = adx.adx()

    return df