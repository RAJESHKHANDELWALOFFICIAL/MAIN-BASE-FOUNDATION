import logging
import os


class LoggerConnection:

    def __init__(self):
        os.makedirs("logs", exist_ok=True)

        self.logger = logging.getLogger("MAIN_BASE_FOUNDATION")

        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)

            file_handler = logging.FileHandler(
                "logs/main_base_foundation.log",
                encoding="utf-8"
            )

            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            )

            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger
