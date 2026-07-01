import yfinance as yf
import pandas as pd

from .config import DEFAULT_PERIOD, DEFAULT_INTERVAL


def fetch_stock_data(
    ticker: str,
    period: str = DEFAULT_PERIOD,
    interval: str = DEFAULT_INTERVAL
) -> pd.DataFrame:
    """
    Fetch historical market data from Yahoo Finance.

    Parameters
    ----------
    ticker : str
        Example: RELIANCE.NS

    period : str
        Example: 5y, 1y, 6mo

    interval : str
        Example: 1d, 1h, 5m

    Returns
    -------
    pd.DataFrame
        Standardized OHLCV dataframe.
    """

    try:

        print(f"[INFO] Downloading market data for {ticker}...")

        data = yf.download(
            tickers=ticker,
            period=period,
            interval=interval,
            auto_adjust=False,
            progress=False
        )

        if data.empty:
            raise ValueError(f"No market data found for {ticker}")

        # Flatten MultiIndex columns if Yahoo returns them
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        # Remove unwanted column header name ("Price")
        data.columns.name = None

        # Convert Date index to column
        data.reset_index(inplace=True)

        # Rename columns
        data.rename(
            columns={
                "Date": "date",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Adj Close": "adj_close",
                "Volume": "volume",
            },
            inplace=True,
        )

        # Standard column order
        data = data[
            [
                "date",
                "open",
                "high",
                "low",
                "close",
                "adj_close",
                "volume",
            ]
        ]

        # Datatypes
        data["date"] = pd.to_datetime(data["date"])

        numeric_columns = [
            "open",
            "high",
            "low",
            "close",
            "adj_close",
            "volume",
        ]

        data[numeric_columns] = data[numeric_columns].apply(
            pd.to_numeric,
            errors="coerce",
        )

        # Remove duplicate dates
        data.drop_duplicates(
            subset="date",
            keep="last",
            inplace=True,
        )

        # Sort chronologically
        data.sort_values(
            by="date",
            inplace=True,
        )

        # Reset index
        data.reset_index(
            drop=True,
            inplace=True,
        )

        print(f"[SUCCESS] Downloaded {len(data)} rows.")

        return data

    except Exception as e:
        raise RuntimeError(
            f"Failed to fetch market data for {ticker}: {e}"
        )