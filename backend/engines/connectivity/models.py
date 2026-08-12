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
class ConnectivityReport:
    """Platform-neutral connectivity report."""

    device: Dict[str, Any] = field(default_factory=dict)

    internet: bool = False
    wifi: bool = False
    ethernet: bool = False
    hotspot: bool = False
    vpn: bool = False

    current_network: Optional[str] = None

    interfaces: List[NetworkInterface] = field(
        default_factory=list
    )

    visible_networks: List[VisibleNetwork] = field(
        default_factory=list
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
            "hotspot": self.hotspot,
            "vpn": self.vpn,
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
            "health": self.health,
            "security": self.security,
            "status": self.status,
            "reason": self.reason,
            "last_check": self.last_check,
            "capabilities": self.capabilities,
        }
