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
