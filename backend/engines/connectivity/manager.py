import platform
from datetime import datetime, timezone
from typing import Dict, List, Optional

from .detectors import ConnectivityDetector
from .models import ConnectivityReport
from .scanner import NetworkScanner
from .security import ConnectivitySecurity

from .platforms.android import AndroidConnectivityPlatform
from .platforms.ios import IOSConnectivityPlatform
from .platforms.linux import LinuxConnectivityPlatform
from .platforms.macos import MacOSConnectivityPlatform
from .platforms.windows import WindowsConnectivityPlatform


class ConnectivityEngine:
    """MAIN BASE FOUNDATION unified connectivity engine."""

    def __init__(self):
        self.detector = ConnectivityDetector()
        self.scanner = NetworkScanner()
        self.security = ConnectivitySecurity()

        self.platform_name = platform.system().upper()

        self.platforms = {
            "WINDOWS": WindowsConnectivityPlatform(),
            "LINUX": LinuxConnectivityPlatform(),
            "DARWIN": MacOSConnectivityPlatform(),
            "ANDROID": AndroidConnectivityPlatform(),
            "IOS": IOSConnectivityPlatform(),
            "IPADOS": IOSConnectivityPlatform(),
        }

        self.report = ConnectivityReport()

    def _platform_adapter(self):
        """Return the adapter for the current platform."""

        return self.platforms.get(
            self.platform_name
        )

    def detect(self) -> dict:
        """Build a unified connectivity report."""

        device = self.detector.device_information()
        state = self.detector.connectivity_state()

        adapter = self._platform_adapter()

        wifi = False
        ethernet = False
        vpn = False
        hotspot = False
        capabilities: Dict[str, bool] = {}

        if adapter:
            capabilities = adapter.capabilities()

            platform_state = adapter.connectivity()

            wifi = bool(
                platform_state.get("wifi") is True
            )

            ethernet = bool(
                platform_state.get("ethernet") is True
            )

            vpn = bool(
                platform_state.get("vpn") is True
            )

            hotspot = bool(
                platform_state.get("hotspot") is True
            )

        visible_networks = self.scanner.scan()

        current_network: Optional[str] = None

        if visible_networks:
            current_network = (
                visible_networks[0].ssid
            )

        network_security = "UNKNOWN"

        if visible_networks:
            network_security = (
                visible_networks[0].security
            )

        security_result = self.security.assess(
            internet=bool(
                state["internet"]
            ),
            wifi=wifi,
            ethernet=ethernet,
            hotspot=hotspot,
            vpn=vpn,
            current_network=current_network,
            network_security=network_security,
        )

        self.report = ConnectivityReport(
            device=device,
            internet=bool(
                state["internet"]
            ),
            wifi=wifi,
            ethernet=ethernet,
            hotspot=hotspot,
            vpn=vpn,
            current_network=current_network,
            interfaces=self.detector.network_interfaces(),
            visible_networks=visible_networks,
            health=str(
                state["health"]
            ),
            security=str(
                security_result["security"]
            ),
            status=str(
                state["status"]
            ),
            reason=str(
                state["reason"]
            ),
            last_check=datetime.now(
                timezone.utc
            ).isoformat(),
            capabilities=capabilities,
        )

        return self.report.to_dict()

    def status(self) -> dict:
        """Return the current connectivity report."""

        return self.detect()

    def networks(self) -> list:
        """Return safely discoverable visible networks."""

        return [
            {
                "ssid": network.ssid,
                "security": network.security,
                "signal": network.signal,
                "channel": network.channel,
                "bssids": network.bssids,
            }
            for network in self.scanner.scan()
        ]

    def health(self) -> dict:
        """Return connectivity health information."""

        report = self.detect()

        return {
            "health": report["health"],
            "security": report["security"],
            "internet": report["internet"],
            "wifi": report["wifi"],
            "ethernet": report["ethernet"],
            "hotspot": report["hotspot"],
            "vpn": report["vpn"],
            "status": report["status"],
            "last_check": report["last_check"],
        }

    def start(self) -> dict:
        """Start the connectivity engine."""

        return self.detect()

    def stop(self) -> dict:
        """Stop the connectivity engine."""

        self.report.status = "STOPPED"

        return self.report.to_dict()

    def restart(self) -> dict:
        """Restart the connectivity engine."""

        self.stop()

        return self.start()
