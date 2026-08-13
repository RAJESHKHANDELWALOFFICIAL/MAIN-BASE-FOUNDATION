import platform
from datetime import datetime, timezone
from typing import Dict, List, Optional

from .detectors import ConnectivityDetector
from .models import (
    ConnectivityReport,
    SatelliteStatus,
)
from .scanner import NetworkScanner
from .security import ConnectivitySecurity
from .server import ServerMonitor
from .satellite import SatelliteMonitor

from .platforms.android import AndroidConnectivityPlatform
from .platforms.ios import IOSConnectivityPlatform
from .platforms.linux import LinuxConnectivityPlatform
from .platforms.macos import MacOSConnectivityPlatform
from .platforms.windows import WindowsConnectivityPlatform


class ConnectivityEngine:
    """MAIN BASE FOUNDATION unified connectivity engine."""

    def __init__(
        self,
        servers: Optional[List[Dict[str, object]]] = None,
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

        platform_state: Dict[str, object] = {}

        if adapter:
            capabilities = adapter.capabilities()

            platform_state = adapter.connectivity()

            wifi = (
                platform_state.get("wifi") is True
            )

            ethernet = (
                platform_state.get("ethernet") is True
            )

            mobile_data = (
                platform_state.get("mobile_data") is True
            )

            vpn = (
                platform_state.get("vpn") is True
            )

            hotspot = (
                platform_state.get("hotspot") is True
            )

        # --------------------------------------------------
        # VISIBLE NETWORKS
        # --------------------------------------------------

        visible_networks = self.scanner.scan()

        # --------------------------------------------------
        # CURRENT NETWORK
        # --------------------------------------------------

        current_network: Optional[str] = None

        adapter_network = platform_state.get(
            "current_network"
        )

        if adapter_network:
            current_network = str(
                adapter_network
            )

        elif visible_networks:
            current_network = (
                visible_networks[0].ssid
            )

        # --------------------------------------------------
        # NETWORK SECURITY
        # --------------------------------------------------

        network_security = "UNKNOWN"

        if visible_networks:
            network_security = (
                visible_networks[0].security
            )

        # --------------------------------------------------
        # SECURITY ASSESSMENT
        # --------------------------------------------------

        security_result = self.security.assess(
            internet=bool(
                state.get("internet", False)
            ),
            wifi=wifi,
            ethernet=ethernet,
            hotspot=hotspot,
            vpn=vpn,
            current_network=current_network,
            network_security=network_security,
        )

        # --------------------------------------------------
        # SERVER MONITORING
        # --------------------------------------------------

        servers = self.server_monitor.check_all()

        # --------------------------------------------------
        # SATELLITE STATUS
        # --------------------------------------------------

        satellite_status = (
            self.satellite_monitor.status()
        )

        satellite_connected = (
            satellite_status.connected
        )

        satellite_online = (
            satellite_status.online
        )

        # --------------------------------------------------
        # ONLINE / OFFLINE
        # --------------------------------------------------

        internet_online = bool(
            state.get("internet", False)
        )

        online = (
            internet_online
            or satellite_online
        )

        offline = not online

        # --------------------------------------------------
        # HEALTH
        # --------------------------------------------------

        health = str(
            state.get(
                "health",
                "UNKNOWN",
            )
        )

        status = str(
            state.get(
                "status",
                "UNKNOWN",
            )
        )

        reason = str(
            state.get(
                "reason",
                "",
            )
        )

        # Satellite can provide connectivity
        # even when normal Internet detection fails.

        if satellite_online:
            online = True
            offline = False
            status = "ONLINE"
            health = "HEALTHY"
            reason = (
                "Satellite connectivity detected."
            )

        # --------------------------------------------------
        # FINAL REPORT
        # --------------------------------------------------

        self.report = ConnectivityReport(
            device=device,

            internet=internet_online,

            wifi=wifi,

            ethernet=ethernet,

            mobile_data=mobile_data,

            hotspot=hotspot,

            vpn=vpn,

            satellite=satellite_connected,

            online=online,

            offline=offline,

            current_network=current_network,

            interfaces=(
                self.detector.network_interfaces()
            ),

            visible_networks=visible_networks,

            servers=servers,

            satellite_status=satellite_status,

            health=health,

            security=str(
                security_result.get(
                    "security",
                    "UNKNOWN",
                )
            ),

            status=status,

            reason=reason,

            last_check=datetime.now(
                timezone.utc
            ).isoformat(),

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
            for server in self.server_monitor.check_all()
        ]

    def satellite(self) -> dict:
        """Return current satellite connectivity status."""

        return {
            "provider": (
                self.report.satellite_status.provider
            ),
            "connected": (
                self.report.satellite_status.connected
            ),
            "online": (
                self.report.satellite_status.online
            ),
            "signal": (
                self.report.satellite_status.signal
            ),
            "latency_ms": (
                self.report.satellite_status.latency_ms
            ),
            "status": (
                self.report.satellite_status.status
            ),
            "source": (
                self.report.satellite_status.source
            ),
        }

    def ingest_satellite(
        self,
        data: Dict[str, object],
    ) -> dict:
        """Ingest approved satellite telemetry."""

        self.satellite_monitor.ingest(data)

        return self.detect()

    def health(self) -> dict:
        """Return connectivity health information."""

        report = self.detect()

        return {
            "health": report["health"],
            "security": report["security"],
            "internet": report["internet"],
            "wifi": report["wifi"],
            "ethernet": report["ethernet"],
            "mobile_data": report["mobile_data"],
            "hotspot": report["hotspot"],
            "vpn": report["vpn"],
            "satellite": report["satellite"],
            "online": report["online"],
            "offline": report["offline"],
            "status": report["status"],
            "last_check": report["last_check"],
        }

    def start(self) -> dict:
        """Start the connectivity engine."""

        return self.detect()

    def stop(self) -> dict:
        """Stop the connectivity engine."""

        self.report.status = "STOPPED"

        self.report.online = False

        self.report.offline = True

        return self.report.to_dict()

    def restart(self) -> dict:
        """Restart the connectivity engine."""

        self.stop()

        return self.start()
