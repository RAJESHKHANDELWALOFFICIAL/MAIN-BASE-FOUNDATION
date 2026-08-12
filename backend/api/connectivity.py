from backend.engines.connectivity.manager import ConnectivityEngine


class ConnectivityAPI:
    """MAIN BASE FOUNDATION Connectivity API."""

    def __init__(self):
        self.engine = ConnectivityEngine()

        def status(self) -> dict:
        """Return the current connectivity status."""

        return self.engine.detect()

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

        status = self.engine.detect()

        return {
            "health": status["health"],
            "security": status["security"],
            "internet": status["internet"],
            "wifi": status["wifi"],
            "ethernet": status["ethernet"],
            "vpn": status["vpn"],
            "last_check": status["last_check"],
        }

    def networks(self) -> list:
        """Return visible Wi-Fi networks without passwords."""

        return self.engine.scan_networks()

