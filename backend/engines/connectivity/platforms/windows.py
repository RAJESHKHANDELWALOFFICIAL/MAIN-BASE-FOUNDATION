import platform
import subprocess
from typing import Dict, List

from ..models import VisibleNetwork
from .base import ConnectivityPlatform


class WindowsConnectivityPlatform(ConnectivityPlatform):
    """Windows connectivity platform adapter."""

    platform_name = "WINDOWS"

    def capabilities(self) -> Dict[str, bool]:
        """Return Windows connectivity capabilities."""

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
        """Return Windows connectivity information."""

        return {
            "platform": platform.system(),
            "wifi": self._wifi_available(),
            "ethernet": self._ethernet_available(),
            "vpn": self._vpn_available(),
            "hotspot": self._hotspot_available(),
        }

    def scan_networks(self) -> List[VisibleNetwork]:
        """Return visible Wi-Fi networks without passwords."""

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

                elif (
                    current_network
                    and line.startswith("Signal")
                ):
                    parts = line.split(":", 1)

                    if len(parts) == 2:
                        current_network.signal = (
                            parts[1].strip()
                        )

                elif (
                    current_network
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

    def _wifi_available(self) -> bool:
        """Check whether a Wi-Fi adapter is available."""

        return self._adapter_contains(
            "wi-fi",
            "wireless",
        )

    def _ethernet_available(self) -> bool:
        """Check whether an Ethernet adapter is available."""

        return self._adapter_contains(
            "ethernet",
        )

    def _vpn_available(self) -> bool:
        """Check whether a VPN adapter appears to be available."""

        return self._adapter_contains(
            "vpn",
            "wireguard",
            "tap",
            "tun",
        )

    def _hotspot_available(self) -> bool:
        """Check whether Windows hotspot capability is detectable."""

        try:
            result = subprocess.run(
                [
                    "netsh",
                    "wlan",
                    "show",
                    "hostednetwork",
                ],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )

            output = result.stdout.lower()

            return (
                "hosted network mode" in output
                or "hosted network status" in output
            )

        except (
            OSError,
            subprocess.SubprocessError,
        ):
            return False

    def _adapter_contains(
        self,
        *keywords: str,
    ) -> bool:
        """Check Windows network adapter information."""

        try:
            result = subprocess.run(
                ["ipconfig", "/all"],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )

            output = result.stdout.lower()

            return any(
                keyword.lower() in output
                for keyword in keywords
            )

        except (
            OSError,
            subprocess.SubprocessError,
        ):
            return False
