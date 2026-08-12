import platform
import subprocess
from typing import List

from .models import VisibleNetwork


class NetworkScanner:
    """Platform-aware safe network discovery service."""

    def __init__(self):
        self.platform = platform.system()

    def scan(self) -> List[VisibleNetwork]:
        """Return visible Wi-Fi networks without collecting passwords."""

        if self.platform == "Windows":
            return self._scan_windows()

        return []

    def _scan_windows(self) -> List[VisibleNetwork]:
        """Scan visible Wi-Fi networks on Windows."""

        networks: List[VisibleNetwork] = []

        try:
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

            if result.returncode != 0:
                return networks

            current_network = None
            current_bssid = None

            for raw_line in result.stdout.splitlines():
                line = raw_line.strip()

                if line.startswith("SSID"):
                    parts = line.split(":", 1)

                    if len(parts) != 2:
                        continue

                    ssid = parts[1].strip()

                    if not ssid:
                        continue

                    current_network = VisibleNetwork(
                        ssid=ssid
                    )

                    networks.append(current_network)
                    current_bssid = None

                elif (
                    current_network
                    and line.startswith("Authentication")
                ):
                    parts = line.split(":", 1)

                    if len(parts) == 2:
                        current_network.security = (
                            parts[1].strip()
                        )

                elif (
                    current_network
                    and line.startswith("BSSID")
                ):
                    parts = line.split(":", 1)

                    if len(parts) == 2:
                        bssid = parts[1].strip()

                        if bssid:
                            current_network.bssids.append(
                                bssid
                            )
                            current_bssid = {
                                "network": current_network,
                                "bssid": bssid,
                            }

                elif (
                    current_bssid
                    and line.startswith("Signal")
                ):
                    parts = line.split(":", 1)

                    if len(parts) == 2:
                        current_network.signal = (
                            parts[1].strip()
                        )

                elif (
                    current_bssid
                    and line.startswith("Channel")
                ):
                    parts = line.split(":", 1)

                    if len(parts) == 2:
                        current_network.channel = (
                            parts[1].strip()
                        )

            return networks

        except (
            OSError,
            subprocess.SubprocessError,
        ):
            return []
