import time

from src.ingestion.symbol_provider import SymbolProvider
from src.ingestion.fetch_yahoo import fetch_stock_data
from src.ingestion.save_data import save_to_csv

from src.preprocessing.validator import DataValidator
from src.preprocessing.cleaner import DataCleaner

from src.utils.logger import PipelineLogger


def main():

    start_time = time.time()

    # Initialize Logger
    logger = PipelineLogger()

    print("=" * 70)
    print("              Algo AI - Market Data Ingestion Pipeline")
    print("=" * 70)

    logger.info("Pipeline Started.")

    # --------------------------------------------------
    # Initialize Components
    # --------------------------------------------------

    provider = SymbolProvider()
    validator = DataValidator()
    cleaner = DataCleaner()

    # --------------------------------------------------
    # Load Symbols
    # --------------------------------------------------

    symbols = provider.get_symbols()

    logger.info(f"Loaded {len(symbols)} symbols.")

    print(f"\nTotal Symbols Found : {len(symbols)}")

    successful_downloads = 0
    failed_downloads = 0
    validation_failures = 0

    failed_stocks = []

    # --------------------------------------------------
    # Process Every Stock
    # --------------------------------------------------

    for index, row in symbols.iterrows():

        symbol = row["symbol"]
        ticker = row["ticker"]
        company = row["company_name"]

        logger.info(f"Processing {symbol} ({ticker})")

        print("\n" + "-" * 70)
        print(f"Stock {index + 1} of {len(symbols)}")
        print(f"Company : {company}")
        print(f"Ticker  : {ticker}")

        try:

            # ======================================================
            # STEP 1 : DOWNLOAD
            # ======================================================

            logger.info(f"Downloading market data for {ticker}")

            df = fetch_stock_data(ticker)

            logger.info(f"Downloaded {len(df)} rows.")

            # ======================================================
            # STEP 2 : VALIDATE RAW DATA
            # ======================================================

            print("\nRaw Data Validation")
            print("=" * 40)

            raw_report = validator.validate(df)

            logger.info(
                f"Raw Validation Score : {raw_report['score']}/{raw_report['total_checks']}"
            )

            print(f"Status               : {'PASS' if raw_report['status'] else 'FAIL'}")
            print(f"Validation Score     : {raw_report['score']} / {raw_report['total_checks']}")
            print(f"Rows                 : {raw_report['rows']}")

            # ======================================================
            # STEP 3 : CLEAN DATA
            # ======================================================

            print("\nCleaning Dataset...")

            clean_df, cleaning_report = cleaner.clean(df)

            logger.info(
                f"Cleaner removed {cleaning_report['rows_removed']} rows."
            )

            print("\nCleaning Report")
            print("=" * 40)

            print(f"Initial Rows         : {cleaning_report['initial_rows']}")
            print(f"Final Rows           : {cleaning_report['final_rows']}")
            print(f"Rows Removed         : {cleaning_report['rows_removed']}")
            print(f"Duplicates Removed   : {cleaning_report['duplicates_removed']}")
            print(f"Future Dates Removed : {cleaning_report['future_dates_removed']}")
            print(f"Missing Rows Removed : {cleaning_report['missing_rows_removed']}")

            # ======================================================
            # STEP 4 : VALIDATE CLEANED DATA
            # ======================================================

            print("\nCleaned Data Validation")
            print("=" * 40)

            report = validator.validate(clean_df)

            logger.info(
                f"Clean Validation Score : {report['score']}/{report['total_checks']}"
            )

            print(f"Status               : {'PASS' if report['status'] else 'FAIL'}")
            print(f"Validation Score     : {report['score']} / {report['total_checks']}")
            print(f"Rows                 : {report['rows']}")

            print("-" * 40)

            print(f"Duplicate Dates      : {report['duplicate_dates']}")
            print(f"Missing Values       : {report['missing_values']}")
            print(f"Negative Prices      : {report['negative_prices']}")
            print(f"High < Low Errors    : {report['price_errors']}")
            print(f"Open Price Errors    : {report['open_price_errors']}")
            print(f"Close Price Errors   : {report['close_price_errors']}")
            print(f"Negative Volume      : {report['negative_volume']}")
            print(f"Future Dates         : {report['future_dates']}")
            print(f"Dates Sorted         : {report['sorted_dates']}")

            # ======================================================
            # STEP 5 : SAVE
            # ======================================================

            if report["status"]:

                save_to_csv(clean_df, symbol)

                successful_downloads += 1

                logger.info(f"{symbol} saved successfully.")

                print(f"\n[SUCCESS] {symbol} cleaned, validated and saved.")

            else:

                validation_failures += 1
                failed_stocks.append(symbol)

                logger.warning(f"{symbol} failed validation.")

                print(f"\n[VALIDATION FAILED] {symbol} was NOT saved.")

        except Exception as e:

            failed_downloads += 1
            failed_stocks.append(symbol)

            logger.error(f"{symbol} failed : {e}")

            print(f"\n[DOWNLOAD FAILED] {symbol}")
            print(f"Reason : {e}")

    # --------------------------------------------------
    # Pipeline Summary
    # --------------------------------------------------

    end_time = time.time()

    logger.info("Pipeline Finished.")

    print("\n")
    print("=" * 70)
    print("                    Pipeline Summary")
    print("=" * 70)

    print(f"Total Stocks          : {len(symbols)}")
    print(f"Downloaded & Saved    : {successful_downloads}")
    print(f"Validation Failed     : {validation_failures}")
    print(f"Download Failed       : {failed_downloads}")
    print(f"Execution Time        : {end_time - start_time:.2f} seconds")

    logger.info(f"Successful : {successful_downloads}")
    logger.info(f"Validation Failed : {validation_failures}")
    logger.info(f"Download Failed : {failed_downloads}")
    logger.info(f"Execution Time : {end_time - start_time:.2f} sec")

    if failed_stocks:

        print("\nFailed Stocks")
        print("-" * 40)

        logger.warning("Failed Stocks:")

        for stock in failed_stocks:
            print(stock)
            logger.warning(stock)

    print("\n" + "=" * 70)
    print("Pipeline Completed Successfully.")
    print("=" * 70)


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    main()