from pathlib import Path

# --------------------------------------------------
# Project Root
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# --------------------------------------------------
# Data Directories
# --------------------------------------------------

DATA_PATH = PROJECT_ROOT / "data"

RAW_DATA_PATH = DATA_PATH / "raw"
PROCESSED_DATA_PATH = DATA_PATH / "processed"
MODELS_PATH = DATA_PATH / "models"
SYMBOLS_PATH = DATA_PATH / "symbols"

# --------------------------------------------------
# Create Directories Automatically
# --------------------------------------------------

RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)
MODELS_PATH.mkdir(parents=True, exist_ok=True)
SYMBOLS_PATH.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Default Download Settings
# --------------------------------------------------

DEFAULT_PERIOD = "5y"
DEFAULT_INTERVAL = "1d"