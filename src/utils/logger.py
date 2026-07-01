import logging
from pathlib import Path
from datetime import datetime


class PipelineLogger:
    """
    Pipeline Logger

    Logs are stored in:

    logs/
        2026-07-01.log
        2026-07-02.log
        ...

    Console output is handled using print().
    Logger writes only to the log file.
    """

    def __init__(self):

        # ---------------------------------------------
        # Create Logs Folder
        # ---------------------------------------------

        log_folder = Path("logs")
        log_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        # ---------------------------------------------
        # Daily Log File
        # ---------------------------------------------

        log_file = log_folder / (
            datetime.now().strftime("%Y-%m-%d") + ".log"
        )

        # ---------------------------------------------
        # Logger Instance
        # ---------------------------------------------

        self.logger = logging.getLogger("AlgoAI")

        self.logger.setLevel(logging.INFO)

        # Prevent duplicate handlers
        if self.logger.handlers:
            return

        # ---------------------------------------------
        # Log Format
        # ---------------------------------------------

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # ---------------------------------------------
        # File Handler ONLY
        # ---------------------------------------------

        file_handler = logging.FileHandler(
            log_file,
            mode="a",
            encoding="utf-8"
        )

        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    # -------------------------------------------------
    # Logging Methods
    # -------------------------------------------------

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)