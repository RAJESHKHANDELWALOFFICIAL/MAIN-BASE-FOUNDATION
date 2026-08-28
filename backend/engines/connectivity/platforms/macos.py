import platform
import subprocess
from typing import Dict, List

from ..models import VisibleNetwork
from .base import ConnectivityPlatform


class MacOSConnectivityPlatform(ConnectivityPlatform):
    """macOS connectivity platform adapter."""

    platform_name = "MACOS"

    def capabilities(self) -> Dict[str, bool]:
        """Return macOS connectivity capabilities."""

        return {
            "wifi_detection": True,
            "wifi_scanning": True,
            "ethernet_detection": True,
            "vpn_detection": True,
            "hotspot_detection": True,
            "network_control": False,
            "password_access": False,
        }

    def connectivity(self) -> Dict[str, object]:
        """Return macOS connectivity information."""

        return {
            "platform": platform.system(),
            "wifi": self._wifi_available(),
            "ethernet": self._ethernet_available(),
            "vpn": self._vpn_available(),
            "hotspot": self._hotspot_available(),
        }

    def scan_networks(self) -> List[VisibleNetwork]:
        """Return visible Wi-Fi networks without collecting passwords."""

        networks: List[VisibleNetwork] = []

        try:
            result = subprocess.run(
                [
                    "/System/Library/PrivateFrameworks/"
                    "Apple80211.framework/Versions/Current/"
                    "Resources/airport",
                    "-s",
                ],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )

            if result.returncode != 0:
                return networks

            lines = result.stdout.splitlines()

            if len(lines) <= 1:
                return networks

            for raw_line in lines[1:]:
                line = raw_line.strip()

                if not line:
                    continue

                parts = line.split()

                if len(parts) < 7:
                    continue

                bssid = parts[1]
                signal = parts[2]
                channel = parts[3]
                security = parts[6]

                ssid = " ".join(parts[7:])

                if not ssid:
                    continue

                network = VisibleNetwork(
                    ssid=ssid,
                    security=security or "UNKNOWN",
                    signal=signal or None,
                    channel=channel or None,
                )

                if bssid:
                    network.bssids.append(bssid)

                networks.append(network)

            return networks

        except (
            OSError,
            subprocess.SubprocessError,
        ):
            return []

    def _wifi_available(self) -> bool:
        """Detect Wi-Fi interface availability."""

        return self._networksetup_contains(
            "Wi-Fi",
        )

    def _ethernet_available(self) -> bool:
        """Detect Ethernet interface availability."""

        return self._networksetup_contains(
            "Ethernet",
        )

    def _vpn_available(self) -> bool:
        """Detect VPN interface availability."""

        return self._networksetup_contains(
            "VPN",
        )

    def _hotspot_available(self) -> bool:
        """Detect whether Wi-Fi hardware is available."""

        try:
            result = subprocess.run(
                [
                    "networksetup",
                    "-listallhardwareports",
                ],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )

            output = result.stdout.lower()

            return (
                "wi-fi" in output
                or "airport" in output
            )

        except (
            OSError,
            subprocess.SubprocessError,
        ):
            return False

    def _networksetup_contains(
        self,
        keyword: str,
    ) -> bool:
        """Search macOS network hardware information."""

        try:
            result = subprocess.run(
                [
                    "networksetup",
                    "-listallhardwareports",
                ],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )

            return keyword.lower() in result.stdout.lower()

        except (
            OSError,
            subprocess.SubprocessError,
        ):
            return False
