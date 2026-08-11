from backend.engines.connectivity.manager import ConnectivityEngine


class ConnectivityAPI:
    """MAIN BASE FOUNDATION Connectivity API."""

    def __init__(self):
        self.engine = ConnectivityEngine()
