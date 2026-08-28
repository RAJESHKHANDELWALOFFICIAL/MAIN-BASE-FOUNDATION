"""MAIN BASE FOUNDATION database API."""

from backend.engines.database import DatabaseEngine


class DatabaseAPI:
    """API facade for the MAIN BASE FOUNDATION database engine."""

    def __init__(self):
        self.engine = DatabaseEngine()

    def status(self) -> dict:
        """Return database status."""

        return self.engine.status()

    def health(self) -> dict:
        """Return database health."""

        return self.engine.health()

    def ping(self) -> dict:
        """Check database connectivity."""

        return self.engine.ping()

    def configuration(self) -> dict:
        """Return safe database configuration information."""

        return self.engine.configuration()

    def connect(self) -> dict:
        """Connect to the configured database."""

        return self.engine.connect()

    def disconnect(self) -> dict:
        """Disconnect from the database."""

        return self.engine.disconnect()
