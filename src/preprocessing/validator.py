import pandas as pd


class DataValidator:
    """
    Validates historical market data before it enters
    the preprocessing and ML pipeline.
    """

    REQUIRED_COLUMNS = [
        "date",
        "open",
        "high",
        "low",
        "close",
        "adj_close",
        "volume",
    ]

    def validate(self, df: pd.DataFrame) -> dict:

        report = {
            "status": True,
            "score": 0,
            "total_checks": 10,
            "rows": len(df),

            "missing_columns": [],
            "duplicate_dates": 0,
            "missing_values": 0,
            "negative_prices": 0,
            "price_errors": 0,
            "open_price_errors": 0,
            "close_price_errors": 0,
            "negative_volume": 0,
            "future_dates": 0,
            "sorted_dates": True,

            "messages": []
        }

        # --------------------------------------------------
        # Check 1 : Empty Dataset
        # --------------------------------------------------
        if df.empty:
            report["status"] = False
            report["messages"].append("Dataset is empty.")
            return report

        report["score"] += 1

        # --------------------------------------------------
        # Check 2 : Required Columns
        # --------------------------------------------------
        for column in self.REQUIRED_COLUMNS:
            if column not in df.columns:
                report["missing_columns"].append(column)

        if report["missing_columns"]:
            report["status"] = False
        else:
            report["score"] += 1

        # Stop if required columns are missing
        if not report["status"]:
            return report

        # --------------------------------------------------
        # Check 3 : Duplicate Dates
        # --------------------------------------------------
        duplicates = df.duplicated(subset="date").sum()

        report["duplicate_dates"] = int(duplicates)

        if duplicates == 0:
            report["score"] += 1

        # --------------------------------------------------
        # Check 4 : Missing Values
        # --------------------------------------------------
        missing = df.isnull().sum().sum()

        report["missing_values"] = int(missing)

        if missing == 0:
            report["score"] += 1

        # --------------------------------------------------
        # Check 5 : Negative Prices
        # --------------------------------------------------
        price_columns = [
            "open",
            "high",
            "low",
            "close",
            "adj_close"
        ]

        negative_prices = (
            df[price_columns] < 0
        ).sum().sum()

        report["negative_prices"] = int(negative_prices)

        if negative_prices == 0:
            report["score"] += 1

        # --------------------------------------------------
        # Check 6 : High must be >= Low
        # --------------------------------------------------
        price_errors = (
            df["high"] < df["low"]
        ).sum()

        report["price_errors"] = int(price_errors)

        if price_errors == 0:
            report["score"] += 1

        # --------------------------------------------------
        # Check 7 : Open within High-Low
        # --------------------------------------------------
        open_errors = (
            (df["open"] > df["high"]) |
            (df["open"] < df["low"])
        ).sum()

        report["open_price_errors"] = int(open_errors)

        if open_errors == 0:
            report["score"] += 1

        # --------------------------------------------------
        # Check 8 : Close within High-Low
        # --------------------------------------------------
        close_errors = (
            (df["close"] > df["high"]) |
            (df["close"] < df["low"])
        ).sum()

        report["close_price_errors"] = int(close_errors)

        if close_errors == 0:
            report["score"] += 1

        # --------------------------------------------------
        # Check 9 : Negative Volume
        # --------------------------------------------------
        negative_volume = (
            df["volume"] < 0
        ).sum()

        report["negative_volume"] = int(negative_volume)

        if negative_volume == 0:
            report["score"] += 1

        # --------------------------------------------------
        # Check 10 : Future Dates
        # --------------------------------------------------
        today = pd.Timestamp.today().normalize()

        future_dates = (
            df["date"] > today
        ).sum()

        report["future_dates"] = int(future_dates)

        if future_dates == 0:
            report["score"] += 1

        # --------------------------------------------------
        # Date Order Check (Informational)
        # --------------------------------------------------
        report["sorted_dates"] = bool(
            df["date"].is_monotonic_increasing
        )

        # --------------------------------------------------
        # Overall Status
        # --------------------------------------------------
        if (
            report["duplicate_dates"] > 0 or
            report["missing_values"] > 0 or
            report["negative_prices"] > 0 or
            report["price_errors"] > 0 or
            report["open_price_errors"] > 0 or
            report["close_price_errors"] > 0 or
            report["negative_volume"] > 0 or
            report["future_dates"] > 0
        ):
            report["status"] = False

        return report