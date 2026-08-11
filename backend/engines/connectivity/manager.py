import socket
import subprocess
import platform
from datetime import datetime, timezone

from backend.engines.base import BaseEngine


class ConnectivityEngine(BaseEngine):
    """MAIN BASE FOUNDATION Connectivity Engine."""

    def __init__(self, name: str = "ConnectivityEngine"):
        super().__init__(name)

        self.internet = False
        self.wifi = False
        self.ethernet = False
        self.vpn = False

        self.health = "UNKNOWN"
        self.security = "UNKNOWN"
        self.last_check = None
