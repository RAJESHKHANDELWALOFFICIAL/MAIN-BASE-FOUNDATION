from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class NetworkInterface:
    """Unified network interface information."""

    name: str
    interface_type: str = "UNKNOWN"
    connected: bool = False
    enabled: bool = True
    address: Optional[str] = None


@dataclass
class VisibleNetwork:
    """Safe information about a visible wireless network."""

    ssid: str
    security: str = "UNKNOWN"
    signal: Optional[str] = None
    channel: Optional[str] = None
    bssids: List[str] = field(default_factory=list)


@dataclass
class ServerStatus:
    """Health status of an explicitly configured server."""

    name: str
    host: str
    port: int
    protocol: str = "TCP"
    online: bool = False
    latency_ms: Optional[float] = None
    status: str = "UNKNOWN"
    error: Optional[str] = None


@dataclass
class SatelliteStatus:
    """Satellite connectivity telemetry status."""

    provider: Optional[str] = None
    connected: bool = False
    online: bool = False
    signal: Optional[str] = None
    latency_ms: Optional[float] = None
    status: str = "UNKNOWN"
    source: str = "UNKNOWN"


@dataclass
class ConnectivityReport:
    """Platform-neutral unified connectivity report."""

    device: Dict[str, Any] = field(
        default_factory=dict
    )

    internet: bool = False
    wifi: bool = False
    ethernet: bool = False
    mobile_data: bool = False
    hotspot: bool = False
    vpn: bool = False

    satellite: bool = False

    online: bool = False
    offline: bool = True

    current_network: Optional[str] = None

    interfaces: List[NetworkInterface] = field(
        default_factory=list
    )

    visible_networks: List[VisibleNetwork] = field(
        default_factory=list
    )

    servers: List[ServerStatus] = field(
        default_factory=list
    )

    satellite_status: SatelliteStatus = field(
        default_factory=SatelliteStatus
    )

    health: str = "UNKNOWN"
    security: str = "UNKNOWN"

    status: str = "UNKNOWN"
    reason: Optional[str] = None
    last_check: Optional[str] = None

    capabilities: Dict[str, bool] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict:
        """Convert the report into a JSON-friendly dictionary."""

        return {
            "device": self.device,

            "internet": self.internet,
            "wifi": self.wifi,
            "ethernet": self.ethernet,
            "mobile_data": self.mobile_data,
            "hotspot": self.hotspot,
            "vpn": self.vpn,

            "satellite": self.satellite,

            "online": self.online,
            "offline": self.offline,

            "current_network": self.current_network,

            "interfaces": [
                {
                    "name": interface.name,
                    "interface_type": interface.interface_type,
                    "connected": interface.connected,
                    "enabled": interface.enabled,
                    "address": interface.address,
                }
                for interface in self.interfaces
            ],

            "visible_networks": [
                {
                    "ssid": network.ssid,
                    "security": network.security,
                    "signal": network.signal,
                    "channel": network.channel,
                    "bssids": network.bssids,
                }
                for network in self.visible_networks
            ],

            "servers": [
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
                for server in self.servers
            ],

            "satellite_status": {
                "provider": self.satellite_status.provider,
                "connected": self.satellite_status.connected,
                "online": self.satellite_status.online,
                "signal": self.satellite_status.signal,
                "latency_ms": self.satellite_status.latency_ms,
                "status": self.satellite_status.status,
                "source": self.satellite_status.source,
            },

            "health": self.health,
            "security": self.security,
            "status": self.status,
            "reason": self.reason,
            "last_check": self.last_check,
            "capabilities": self.capabilities,
        }
