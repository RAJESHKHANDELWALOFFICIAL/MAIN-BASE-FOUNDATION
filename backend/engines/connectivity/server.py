import socket
import time
from typing import Dict, List, Optional

from .models import ServerStatus


class ServerMonitor:
    """Monitor explicitly configured servers."""

    def __init__(
        self,
        servers: Optional[
            List[Dict[str, object]]
        ] = None,
    ):
        self.servers = servers or []

    def check(
        self,
        name: str,
        host: str,
        port: int,
        protocol: str = "TCP",
        timeout: float = 3.0,
    ) -> ServerStatus:
        """Check one explicitly configured server."""

        started = time.perf_counter()

        try:
            with socket.create_connection(
                (host, port),
                timeout=timeout,
            ):
                latency = (
                    time.perf_counter() - started
                ) * 1000

                return ServerStatus(
                    name=name,
                    host=host,
                    port=port,
                    protocol=protocol.upper(),
                    online=True,
                    latency_ms=round(
                        latency,
                        2,
                    ),
                    status="ONLINE",
                )

        except OSError as exc:
            return ServerStatus(
                name=name,
                host=host,
                port=port,
                protocol=protocol.upper(),
                online=False,
                status="OFFLINE",
                error=str(exc),
            )

    def check_all(self) -> List[ServerStatus]:
        """Check all configured servers."""

        results: List[ServerStatus] = []

        for item in self.servers:
            name = str(
                item.get(
                    "name",
                    "SERVER",
                )
            )

            host = str(
                item.get(
                    "host",
                    "",
                )
            ).strip()

            if not host:
                continue

            try:
                port = int(
                    item.get(
                        "port",
                        443,
                    )
                )

            except (TypeError, ValueError):
                port = 443

            protocol = str(
                item.get(
                    "protocol",
                    "TCP",
                )
            )

            results.append(
                self.check(
                    name=name,
                    host=host,
                    port=port,
                    protocol=protocol,
                )
            )

        return results
