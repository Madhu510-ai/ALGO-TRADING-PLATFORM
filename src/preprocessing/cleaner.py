import pandas as pd


class DataCleaner:
    """
    Cleans historical market data before
    feature engineering and ML.
    """

    PRICE_COLUMNS = [
        "open",
        "high",
        "low",
        "close",
        "adj_close"
    ]

    def clean(
        self,
        df: pd.DataFrame
    ) -> tuple[pd.DataFrame, dict]:

        cleaned = df.copy()

        # -----------------------------
        # Initial Statistics
        # -----------------------------

        initial_rows = len(cleaned)

        duplicate_count = cleaned.duplicated(
            subset="date"
        ).sum()

        # -----------------------------
        # Remove Duplicate Dates
        # -----------------------------

        cleaned.drop_duplicates(
            subset="date",
            keep="first",
            inplace=True
        )

        # -----------------------------
        # Convert Date Column
        # -----------------------------

        cleaned["date"] = pd.to_datetime(
            cleaned["date"]
        )

        # -----------------------------
        # Sort Dates
        # -----------------------------

        cleaned.sort_values(
            by="date",
            inplace=True
        )

        # -----------------------------
        # Remove Future Dates
        # -----------------------------

        today = pd.Timestamp.today().normalize()

        future_dates_removed = (
            cleaned["date"] > today
        ).sum()

        cleaned = cleaned[
            cleaned["date"] <= today
        ]

        # -----------------------------
        # Convert Numeric Columns
        # -----------------------------

        numeric_columns = self.PRICE_COLUMNS + [
            "volume"
        ]

        cleaned[numeric_columns] = cleaned[
            numeric_columns
        ].apply(
            pd.to_numeric,
            errors="coerce"
        )

        # -----------------------------
        # Remove Missing OHLC Rows
        # -----------------------------

        before = len(cleaned)

        cleaned.dropna(
            subset=self.PRICE_COLUMNS,
            inplace=True
        )

        missing_rows_removed = before - len(cleaned)

        # -----------------------------
        # Remove Invalid OHLC
        # -----------------------------

        cleaned = cleaned[
            cleaned["high"] >= cleaned["low"]
        ]

        cleaned = cleaned[
            (cleaned["open"] >= cleaned["low"]) &
            (cleaned["open"] <= cleaned["high"])
        ]

        cleaned = cleaned[
            (cleaned["close"] >= cleaned["low"]) &
            (cleaned["close"] <= cleaned["high"])
        ]

        # -----------------------------
        # Remove Negative Volume
        # -----------------------------

        cleaned = cleaned[
            cleaned["volume"] >= 0
        ]

        # -----------------------------
        # Reset Index
        # -----------------------------

        cleaned.reset_index(
            drop=True,
            inplace=True
        )

        final_rows = len(cleaned)

        # -----------------------------
        # Cleaning Report
        # -----------------------------

        cleaning_report = {

            "initial_rows": initial_rows,

            "final_rows": final_rows,

            "rows_removed": initial_rows - final_rows,

            "duplicates_removed": int(duplicate_count),

            "future_dates_removed": int(future_dates_removed),

            "missing_rows_removed": int(missing_rows_removed)

        }

        return cleaned, cleaning_report