from typing import Dict, List, Optional

from ..models import VisibleNetwork
from .base import ConnectivityPlatform


class IOSConnectivityPlatform(ConnectivityPlatform):
    """iOS and iPadOS connectivity platform adapter."""

    platform_name = "IOS_IPADOS"

    def capabilities(self) -> Dict[str, bool]:
        """Return iOS/iPadOS connectivity capabilities."""

        return {
            "wifi_detection": True,
            "wifi_scanning": False,
            "ethernet_detection": True,
            "vpn_detection": True,
            "hotspot_detection": True,
            "network_control": False,
            "password_access": False,
            "native_api_required": True,
            "runtime_permission_required": True,
        }

    def connectivity(self) -> Dict[str, object]:
        """Return iOS/iPadOS connectivity information."""

        return {
            "platform": self.platform_name,
            "status": "NATIVE_CLIENT_REQUIRED",
            "wifi": None,
            "ethernet": None,
            "vpn": None,
            "hotspot": None,
            "permission_required": True,
        }

    def scan_networks(self) -> List[VisibleNetwork]:
        """Return native iOS/iPadOS scan data when available."""

        return []

    def ingest_native_scan(
        self,
        networks: List[Dict[str, object]],
    ) -> List[VisibleNetwork]:
        """Convert approved native client network data."""

        result: List[VisibleNetwork] = []

        for item in networks:
            ssid = str(item.get("ssid", "")).strip()

            if not ssid:
                continue

            network = VisibleNetwork(
                ssid=ssid,
                security=str(
                    item.get("security", "UNKNOWN")
                ),
                signal=self._optional_string(
                    item.get("signal")
                ),
                channel=self._optional_string(
                    item.get("channel")
                ),
            )

            bssid = self._optional_string(
                item.get("bssid")
            )

            if bssid:
                network.bssids.append(bssid)

            result.append(network)

        return result

    @staticmethod
    def _optional_string(
        value: object,
    ) -> Optional[str]:
        """Convert an optional value to a string."""

        if value is None:
            return None

        text = str(value).strip()

        return text or None
