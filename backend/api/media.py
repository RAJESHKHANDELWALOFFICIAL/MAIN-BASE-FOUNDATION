"""MAIN BASE FOUNDATION media API."""

from backend.engines.media import MediaEngine


class MediaAPI:
    """API facade for the MAIN BASE FOUNDATION media engine."""

    def __init__(self):
        self.engine = MediaEngine()

    def status(self) -> dict:
        """Return media status."""

        return self.engine.status()

    def health(self) -> dict:
        """Return media health."""

        return self.engine.health()

    def configuration(self) -> dict:
        """Return safe media configuration."""

        return self.engine.configuration()

    def connect(self) -> dict:
        """Connect to the media layer."""

        return self.engine.connect()

    def disconnect(self) -> dict:
        """Disconnect from the media layer."""

        return self.engine.disconnect()
