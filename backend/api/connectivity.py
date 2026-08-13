from typing import Dict

from backend.engines.connectivity.manager import ConnectivityEngine


class ConnectivityAPI:
    """MAIN BASE FOUNDATION Connectivity API."""

    def __init__(self):
        self.engine = ConnectivityEngine()

    def status(self) -> dict:
        """Return the current unified connectivity status."""

        return self.engine.status()

    def start(self) -> dict:
        """Start the connectivity engine."""

        return self.engine.start()

    def stop(self) -> dict:
        """Stop the connectivity engine."""

        return self.engine.stop()

    def restart(self) -> dict:
        """Restart the connectivity engine."""

        return self.engine.restart()

    def health(self) -> dict:
        """Return connectivity health information."""

        return self.engine.health()

    def networks(self) -> list:
        """Return visible networks without passwords."""

        return self.engine.networks()

    def servers(self) -> list:
        """Return configured server health information."""

        return self.engine.servers()

    def satellite(self) -> dict:
        """Return current satellite connectivity status."""

        return self.engine.satellite()

    def ingest_satellite(
        self,
        data: Dict[str, object],
    ) -> dict:
        """Ingest approved satellite telemetry."""

        return self.engine.ingest_satellite(data)
