import platform
import shutil
import subprocess
from typing import Dict, List

from ..models import VisibleNetwork
from .base import ConnectivityPlatform


class LinuxConnectivityPlatform(ConnectivityPlatform):
    """Linux connectivity platform adapter."""

    platform_name = "LINUX"

    def capabilities(self) -> Dict[str, bool]:
        """Return Linux connectivity capabilities."""

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
        """Return Linux connectivity information."""

        return {
            "platform": platform.system(),
            "wifi": self._interface_available(
                "wifi"
            ),
            "ethernet": self._interface_available(
                "ethernet"
            ),
            "vpn": self._interface_available(
                "vpn"
            ),
            "hotspot": self._hotspot_available(),
        }

    def scan_networks(self) -> List[VisibleNetwork]:
        """Return visible Wi-Fi networks without passwords."""

        if not shutil.which("nmcli"):
            return []

        networks: List[VisibleNetwork] = []

        try:
            result = subprocess.run(
                [
                    "nmcli",
                    "-t",
                    "-f",
                    "SSID,SECURITY,SIGNAL,CHAN,BSSID",
                    "device",
                    "wifi",
                    "list",
                ],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )

            if result.returncode != 0:
                return networks

            for raw_line in result.stdout.splitlines():
                if not raw_line.strip():
                    continue

                parts = raw_line.split(":")

                if len(parts) < 5:
                    continue

                ssid = parts[0].strip()
                security = parts[1].strip() or "OPEN"
                signal = parts[2].strip() or None
                channel = parts[3].strip() or None
                bssid = parts[4].strip()

                if not ssid:
                    continue

                network = VisibleNetwork(
                    ssid=ssid,
                    security=security,
                    signal=signal,
                    channel=channel,
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

    def _interface_available(
        self,
        interface_type: str,
    ) -> bool:
        """Check whether a Linux network interface exists."""

        if not shutil.which("ip"):
            return False

        try:
            result = subprocess.run(
                ["ip", "-o", "link", "show"],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )

            output = result.stdout.lower()

            if interface_type == "wifi":
                return any(
                    keyword in output
                    for keyword in (
                        "wlan",
                        "wifi",
                        "wireless",
                    )
                )

            if interface_type == "ethernet":
                return any(
                    keyword in output
                    for keyword in (
                        "eth",
                        "enp",
                        "eno",
                    )
                )

            if interface_type == "vpn":
                return any(
                    keyword in output
                    for keyword in (
                        "tun",
                        "tap",
                        "wg",
                    )
                )

            return False

        except (
            OSError,
            subprocess.SubprocessError,
        ):
            return False

    def _hotspot_available(self) -> bool:
        """Detect whether a Wi-Fi hotspot capability is available."""

        if not shutil.which("nmcli"):
            return False

        try:
            result = subprocess.run(
                [
                    "nmcli",
                    "-t",
                    "-f",
                    "TYPE",
                    "device",
                ],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )

            return "wifi" in result.stdout.lower()

        except (
            OSError,
            subprocess.SubprocessError,
        ):
            return False
