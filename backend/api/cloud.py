from typing import Dict, Optional

from backend.engines.cloud.manager import CloudEngine


class CloudAPI:
    """MAIN BASE FOUNDATION Cloud API."""

    def __init__(self):
        self.engine = CloudEngine()

    def status(self) -> dict:
        """Return unified cloud status."""

        return self.engine.status()

    def health(self) -> dict:
        """Return cloud infrastructure health."""

        return self.engine.health()

    def security(self) -> dict:
        """Return cloud integration security."""

        return self.engine.security()

    def providers(self) -> list:
        """Return registered cloud providers."""

        return [
            provider.to_dict()
            for provider in self.engine.providers()
        ]

    def provider(self, name: str) -> dict:
        """Return one cloud provider."""

        return self.engine.provider(name).to_dict()

    def summary(self) -> Dict[str, object]:
        """Return compact cloud summary."""

        return self.engine.summary()

    def configure(
        self,
        provider: str,
        region: Optional[str] = None,
    ) -> dict:
        """Register provider configuration."""

        return self.engine.configure(
            provider=provider,
            region=region,
        )

    def authorize(
        self,
        provider: str,
    ) -> dict:
        """Record authorization from an approved flow."""

        return self.engine.authorize(
            provider=provider,
        )

    def set_online(
        self,
        provider: str,
        online: bool,
        latency_ms: Optional[float] = None,
    ) -> dict:
        """Update provider availability telemetry."""

        return self.engine.set_online(
            provider=provider,
            online=online,
            latency_ms=latency_ms,
        )

    def services(
        self,
        provider: str,
    ) -> list:
        """Return services registered for a provider."""

        return self.engine.services(provider)

    def start(self) -> dict:
        """Start cloud monitoring."""

        return self.engine.start()

    def stop(self) -> dict:
        """Stop cloud monitoring."""

        return self.engine.stop()

    def restart(self) -> dict:
        """Restart cloud monitoring."""

        return self.engine.restart()
