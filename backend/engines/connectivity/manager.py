import platform
from datetime import datetime, timezone
from typing import Dict, List, Optional

from .detectors import ConnectivityDetector
from .models import (
    ConnectivityReport,
    ServerStatus,
    SatelliteStatus,
)
from .scanner import NetworkScanner
from .security import ConnectivitySecurity
from .satellite import SatelliteMonitor
from .server import ServerMonitor

from .platforms.android import AndroidConnectivityPlatform
from .platforms.ios import IOSConnectivityPlatform
from .platforms.linux import LinuxConnectivityPlatform
from .platforms.macos import MacOSConnectivityPlatform
from .platforms.windows import WindowsConnectivityPlatform


class ConnectivityEngine:
    """MAIN BASE FOUNDATION unified connectivity engine."""

    def __init__(
        self,
        servers: Optional[
            List[Dict[str, object]]
        ] = None,
        satellite_provider: Optional[str] = None,
    ):
        self.detector = ConnectivityDetector()
        self.scanner = NetworkScanner()
        self.security = ConnectivitySecurity()

        self.server_monitor = ServerMonitor(
            servers=servers or []
        )

        self.satellite_monitor = SatelliteMonitor(
            provider=satellite_provider
        )

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
        mobile_data = False
        vpn = False
        hotspot = False

        capabilities: Dict[str, bool] = {}

        if adapter:
            capabilities = adapter.capabilities()

            platform_state = adapter.connectivity()

            wifi = (
                platform_state.get("wifi")
                is True
            )

            ethernet = (
                platform_state.get("ethernet")
                is True
            )

            mobile_data = (
                platform_state.get("mobile_data")
                is True
            )

            vpn = (
                platform_state.get("vpn")
                is True
            )

            hotspot = (
                platform_state.get("hotspot")
                is True
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

        internet = bool(
            state.get("internet", False)
        )

        online = bool(
            state.get("online", internet)
        )

        offline = not online

        server_results = (
            self.server_monitor.check_all()
        )

        satellite_status = (
            self.satellite_monitor.status()
        )

        satellite_online = bool(
            satellite_status.online
        )

        security_result = self.security.assess(
            internet=internet,
            wifi=wifi,
            ethernet=ethernet,
            hotspot=hotspot,
            vpn=vpn,
            current_network=current_network,
            network_security=network_security,
        )

        self.report = ConnectivityReport(
            device=device,

            internet=internet,
            wifi=wifi,
            ethernet=ethernet,
            mobile_data=mobile_data,
            hotspot=hotspot,
            vpn=vpn,

            satellite=satellite_online,

            online=online,
            offline=offline,

            current_network=current_network,

            interfaces=(
                self.detector.network_interfaces()
            ),

            visible_networks=visible_networks,

            servers=server_results,

            satellite_status=satellite_status,

            health=str(
                state.get(
                    "health",
                    "UNKNOWN",
                )
            ),

            security=str(
                security_result.get(
                    "security",
                    "UNKNOWN",
                )
            ),

            status=str(
                state.get(
                    "status",
                    "UNKNOWN",
                )
            ),

            reason=state.get(
                "reason"
            ),

            last_check=(
                datetime.now(
                    timezone.utc
                ).isoformat()
            ),

            capabilities=capabilities,
        )

        return self.report.to_dict()

    def status(self) -> dict:
        """Return the current unified connectivity report."""

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

    def servers(self) -> list:
        """Return configured server health information."""

        return [
            {
                "name": server.name,
                "host": server.host,
                "port": server.port,
                "protocol": server.protocol,
                "online": server.online,
                "latency_ms": server.latency_ms,
                "status": server.status,
                "error": server.error,
            }
            for server in (
                self.server_monitor.check_all()
            )
        ]

    def satellite(self) -> dict:
        """Return current satellite connectivity status."""

        status = (
            self.satellite_monitor.status()
        )

        return {
            "provider": status.provider,
            "connected": status.connected,
            "online": status.online,
            "signal": status.signal,
            "latency_ms": status.latency_ms,
            "status": status.status,
            "source": status.source,
        }

    def ingest_satellite(
        self,
        data: Dict[str, object],
    ) -> dict:
        """Ingest approved satellite telemetry."""

        status = (
            self.satellite_monitor.ingest(
                data
            )
        )

        return {
            "provider": status.provider,
            "connected": status.connected,
            "online": status.online,
            "signal": status.signal,
            "latency_ms": status.latency_ms,
            "status": status.status,
            "source": status.source,
        }

    def health(self) -> dict:
        """Return connectivity health information."""

        report = self.detect()

        return {
            "health": report["health"],
            "security": report["security"],

            "internet": report["internet"],
            "online": report["online"],
            "offline": report["offline"],

            "wifi": report["wifi"],
            "ethernet": report["ethernet"],
            "mobile_data": report["mobile_data"],
            "hotspot": report["hotspot"],
            "vpn": report["vpn"],

            "satellite": report["satellite"],

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
