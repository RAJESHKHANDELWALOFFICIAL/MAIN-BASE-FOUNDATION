import platform
import socket
from datetime import datetime, timezone
from typing import Dict, List

from .models import NetworkInterface


class ConnectivityDetector:
    """Platform-neutral local connectivity detector."""

    def __init__(self):
        self.platform = platform.system()

    def device_information(self) -> Dict[str, str]:
        """Return basic device and operating-system information."""

        return {
            "platform": self.platform,
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "hostname": socket.gethostname(),
        }

    def internet_available(self) -> bool:
        """Check whether external Internet connectivity is reachable."""

        targets = (
            ("1.1.1.1", 53),
            ("8.8.8.8", 53),
        )

        for host, port in targets:
            try:
                with socket.create_connection(
                    (host, port),
                    timeout=3,
                ):
                    return True
            except OSError:
                continue

        return False

    def network_interfaces(self) -> List[NetworkInterface]:
        """Return basic locally visible network interfaces."""

        interfaces: List[NetworkInterface] = []

        try:
            hostname = socket.gethostname()
            addresses = socket.gethostbyname_ex(hostname)[2]

            for index, address in enumerate(addresses):
                interfaces.append(
                    NetworkInterface(
                        name=f"interface-{index + 1}",
                        interface_type="IP",
                        connected=True,
                        enabled=True,
                        address=address,
                    )
                )

        except OSError:
            pass

        return interfaces

    def connectivity_state(self) -> Dict[str, object]:
        """Return a basic connectivity state snapshot."""

        internet = self.internet_available()

        if internet:
            health = "HEALTHY"
            status = "ONLINE"
            reason = "External connectivity detected."
        else:
            health = "OFFLINE"
            status = "OFFLINE"
            reason = "External connectivity was not detected."

        return {
            "internet": internet,
            "health": health,
            "status": status,
            "reason": reason,
            "last_check": datetime.now(
                timezone.utc
            ).isoformat(),
        }
