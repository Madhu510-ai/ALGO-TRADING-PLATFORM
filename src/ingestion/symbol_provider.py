import pandas as pd
from pathlib import Path


class SymbolProvider:

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        self.symbol_directory = (
            self.project_root /
            "data" /
            "symbols"
        )

    def get_symbols(
        self,
        exchange: str = "NSE"
    ) -> pd.DataFrame:

        file_path = self.symbol_directory / f"{exchange}.csv"

        if not file_path.exists():

            raise FileNotFoundError(
                f"{exchange}.csv not found."
            )

        df = pd.read_csv(file_path)

        required_columns = [
            "symbol",
            "ticker",
            "company_name"
        ]

        missing = [
            col
            for col in required_columns
            if col not in df.columns
        ]

        if missing:

            raise ValueError(
                f"Missing columns: {missing}"
            )

        print(f"[SUCCESS] Loaded {len(df)} symbols.")

        return df