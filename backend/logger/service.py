from backend.logger.connection import LoggerConnection


class LoggerService:

    def __init__(self):
        self.logger = LoggerConnection().get_logger()

    def info(self, module, message):
        self.logger.info(f"[{module}] {message}")

    def warning(self, module, message):
        self.logger.warning(f"[{module}] {message}")

    def error(self, module, message):
        self.logger.error(f"[{module}] {message}")

    def critical(self, module, message):
        self.logger.critical(f"[{module}] {message}")
