from typing import Dict, Optional

from .models import SatelliteStatus


class SatelliteMonitor:
    """Satellite connectivity telemetry adapter."""

    def __init__(
        self,
        provider: Optional[str] = None,
    ):
        self.provider = provider

        self.current_status = SatelliteStatus(
            provider=provider,
            connected=False,
            online=False,
            status="NOT_CONFIGURED",
            source="CONFIGURATION",
        )

    def status(self) -> SatelliteStatus:
        """Return the current satellite connectivity status."""

        return self.current_status

    def ingest(
        self,
        data: Dict[str, object],
    ) -> SatelliteStatus:
        """Accept approved satellite telemetry."""

        self.current_status = SatelliteStatus(
            provider=str(
                data.get(
                    "provider",
                    self.provider or "UNKNOWN",
                )
            ),
            connected=bool(
                data.get("connected", False)
            ),
            online=bool(
                data.get("online", False)
            ),
            signal=self._optional_string(
                data.get("signal")
            ),
            latency_ms=self._optional_float(
                data.get("latency_ms")
            ),
            status=str(
                data.get(
                    "status",
                    "UNKNOWN",
                )
            ),
            source=str(
                data.get(
                    "source",
                    "NATIVE_OR_PROVIDER_API",
                )
            ),
        )

        return self.current_status

    @staticmethod
    def _optional_string(
        value: object,
    ) -> Optional[str]:
        """Convert an optional value to a string."""

        if value is None:
            return None

        text = str(value).strip()

        return text or None

    @staticmethod
    def _optional_float(
        value: object,
    ) -> Optional[float]:
        """Convert an optional value to a float."""

        if value is None:
            return None

        try:
            return float(value)

        except (TypeError, ValueError):
            return None
