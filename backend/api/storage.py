"""MAIN BASE FOUNDATION storage API."""

from backend.engines.storage import StorageEngine


class StorageAPI:
    """API facade for the MAIN BASE FOUNDATION storage engine."""

    def __init__(self):
        self.engine = StorageEngine()

    def status(self) -> dict:
        """Return storage status."""

        return self.engine.status()

    def health(self) -> dict:
        """Return storage health."""

        return self.engine.health()

    def configuration(self) -> dict:
        """Return safe storage configuration."""

        return self.engine.configuration()

    def connect(self) -> dict:
        """Initialize the storage layer."""

        return self.engine.connect()

    def disconnect(self) -> dict:
        """Disconnect from the storage layer."""

        return self.engine.disconnect()
