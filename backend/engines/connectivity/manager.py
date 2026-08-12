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

    def _adapter_information(self) -> str:
        """Get local network adapter information."""

        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["ipconfig"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=False,
                )
            else:
                result = subprocess.run(
                    ["ip", "addr"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=False,
                )

            return result.stdout.lower()

        except (OSError, subprocess.SubprocessError):
            return ""

    def _check_internet(self) -> bool:
        """Check whether Internet connectivity is available."""

        try:
            socket.create_connection(
                ("1.1.1.1", 53),
                timeout=3,
            )
            return True

        except OSError:
            return False

    def detect(self) -> dict:
        """Detect current connectivity status."""

        adapters = self._adapter_information()

        self.internet = self._check_internet()

        self.wifi = (
            "wi-fi" in adapters
            or "wireless lan adapter" in adapters
        )

        self.ethernet = (
            "ethernet adapter" in adapters
            or "ethernet" in adapters
        )

        self.vpn = any(
            keyword in adapters
            for keyword in (
                "vpn",
                "wireguard",
                "tap adapter",
                "tun",
            )
        )

        if self.internet:
            self.health = "HEALTHY"
        elif self.wifi or self.ethernet or self.vpn:
            self.health = "WARNING"
        else:
            self.health = "OFFLINE"

        self.security = "UNKNOWN"
        self.last_check = datetime.now(timezone.utc).isoformat()

        return self.connectivity_status()

    def connectivity_status(self) -> dict:
        """Return the current connectivity report."""

        return {
            "engine": self.name,
            "state": self.state,
            "internet": self.internet,
            "wifi": self.wifi,
            "ethernet": self.ethernet,
            "vpn": self.vpn,
            "health": self.health,
            "security": self.security,
            "last_check": self.last_check,
        }

    def scan_networks(self) -> list:
        """Scan visible Wi-Fi networks without collecting passwords."""

        networks = []

        try:
            if platform.system() != "Windows":
                return networks

            result = subprocess.run(
                [
                    "netsh",
                    "wlan",
                    "show",
                    "networks",
                    "mode=bssid",
                ],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )

            output = result.stdout
            current_network = None

            for line in output.splitlines():
                line = line.strip()

                if line.startswith("SSID"):
                    parts = line.split(":", 1)

                    if len(parts) == 2:
                        ssid = parts[1].strip()

                        if ssid:
                            current_network = {
                                "ssid": ssid,
                                "security": "UNKNOWN",
                            }
                            networks.append(current_network)

                elif (
                    current_network
                    and "Authentication" in line
                ):
                    parts = line.split(":", 1)

                    if len(parts) == 2:
                        current_network["security"] = parts[1].strip()

            return networks

        except (OSError, subprocess.SubprocessError):
            return []

    def start(self) -> dict:
        """Start the engine and perform initial detection."""

        super().start()
        self.detect()

        return self.connectivity_status()

    def stop(self) -> dict:
        """Stop the engine."""

        super().stop()

        return self.connectivity_status()

    def restart(self) -> dict:
        """Restart the engine and refresh connectivity state."""

        self.stop()
        return self.start()


if __name__ == "__main__":
    engine = ConnectivityEngine()

    print("=" * 60)
    print("MAIN BASE FOUNDATION")
    print("CONNECTIVITY ENGINE")
    print("=" * 60)

    print(engine.start())

    print("=" * 60)
    print("VISIBLE WI-FI NETWORKS")
    print("=" * 60)

    print(engine.scan_networks())

    print("=" * 60)
