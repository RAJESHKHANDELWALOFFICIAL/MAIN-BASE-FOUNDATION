from datetime import datetime, timezone
from typing import Dict, Optional

from .health import CloudHealthMonitor
from .models import (
    CloudProviderStatus,
    CloudReport,
)
from .providers import CloudProviderRegistry
from .security import CloudSecurityMonitor


class CloudEngine:
    """MAIN BASE FOUNDATION unified cloud engine."""

    def __init__(self):
        self.registry = CloudProviderRegistry()
        self.health_monitor = CloudHealthMonitor()
        self.security_monitor = CloudSecurityMonitor()

        self.report = CloudReport(
            capabilities={
                "provider_registry": True,
                "provider_health": True,
                "provider_security": True,
                "aws": True,
                "google_cloud": True,
                "microsoft_azure": True,
                "cloudflare": True,
                "credential_storage": False,
                "automatic_authentication": False,
            }
        )

    def providers(self) -> list:
        """Return all registered cloud providers."""

        return self.registry.list()

    def provider(
        self,
        name: str,
    ) -> CloudProviderStatus:
        """Return one registered cloud provider."""

        return self.registry.get(name)

    def status(self) -> dict:
        """Return the current unified cloud status."""

        return self.detect()

    def detect(self) -> dict:
        """Build a unified cloud infrastructure report."""

        providers = self.registry.list()

        health = self.health_monitor.assess(
            providers
        )

        security = self.security_monitor.assess(
            providers
        )

        online = any(
            provider.online
            for provider in providers
        )

        if online:
            status = "ONLINE"
            reason = "At least one cloud provider is online."

        elif providers:
            status = "READY"
            reason = (
                "Cloud providers are registered but "
                "no provider is currently authenticated "
                "and online."
            )

        else:
            status = "UNKNOWN"
            reason = "No cloud providers are registered."

        self.report = CloudReport(
            providers=providers,
            health=health,
            online=online,
            offline=not online,
            status=status,
            reason=reason,
            capabilities=self.report.capabilities,
            last_check=datetime.now(
                timezone.utc
            ).isoformat(),
        )

        return self.report.to_dict()

    def health(self) -> dict:
        """Return cloud infrastructure health."""

        report = self.detect()

        return report["health"]

    def security(self) -> dict:
        """Return cloud integration security."""

        providers = self.registry.list()

        return self.security_monitor.assess(
            providers
        )

    def configure(
        self,
        provider: str,
        region: Optional[str] = None,
    ) -> dict:
        """
        Mark a provider as configured.

        This does not store credentials or secrets.
        """

        cloud_provider = self.registry.get(
            provider
        )

        cloud_provider.configured = True
        cloud_provider.region = region
        cloud_provider.status = (
            "CONFIGURED"
        )
        cloud_provider.message = (
            "Provider configuration registered. "
            "Authentication is still required."
        )

        return cloud_provider.to_dict()

    def authorize(
        self,
        provider: str,
    ) -> dict:
        """
        Mark a provider as authorized by an
        external approved authentication flow.

        Credentials are never accepted or stored here.
        """

        cloud_provider = self.registry.get(
            provider
        )

        if not cloud_provider.configured:
            cloud_provider.status = (
                "NOT_CONFIGURED"
            )

            cloud_provider.message = (
                "Configure the provider before "
                "authorization."
            )

            return cloud_provider.to_dict()

        cloud_provider.authenticated = True
        cloud_provider.available = True
        cloud_provider.status = (
            "AUTHORIZED"
        )
        cloud_provider.message = (
            "Provider authorization confirmed "
            "by an approved external flow."
        )

        return cloud_provider.to_dict()

    def set_online(
        self,
        provider: str,
        online: bool,
        latency_ms: Optional[float] = None,
    ) -> dict:
        """
        Update provider availability telemetry.

        This method does not establish a network connection.
        """

        cloud_provider = self.registry.get(
            provider
        )

        cloud_provider.online = bool(
            online
        )

        cloud_provider.available = bool(
            online
        )

        cloud_provider.services = (
            cloud_provider.services
        )

        if online:
            cloud_provider.status = "ONLINE"
            cloud_provider.message = (
                "Provider availability telemetry "
                "reports the provider as online."
            )
        else:
            cloud_provider.status = "OFFLINE"
            cloud_provider.message = (
                "Provider availability telemetry "
                "reports the provider as offline."
            )

        for service in cloud_provider.services:
            service.online = bool(online)
            service.available = bool(online)
            service.latency_ms = latency_ms

        return cloud_provider.to_dict()

    def services(
        self,
        provider: str,
    ) -> list:
        """Return services registered for a provider."""

        cloud_provider = self.registry.get(
            provider
        )

        return [
            service.to_dict()
            for service in cloud_provider.services
        ]

    def summary(self) -> Dict[str, object]:
        """Return a compact cloud infrastructure summary."""

        report = self.detect()

        return {
            "status": report["status"],
            "online": report["online"],
            "offline": report["offline"],
            "health": report["health"]["status"],
            "security": self.security()[
                "security"
            ],
            "total_providers": report[
                "health"
            ]["total_providers"],
            "configured_providers": report[
                "health"
            ]["configured_providers"],
            "authenticated_providers": report[
                "health"
            ]["authenticated_providers"],
            "online_providers": report[
                "health"
            ]["online_providers"],
            "last_check": report[
                "last_check"
            ],
        }

    def start(self) -> dict:
        """Start cloud monitoring."""

        return self.detect()

    def stop(self) -> dict:
        """Stop cloud monitoring."""

        self.report.status = "STOPPED"
        self.report.online = False
        self.report.offline = True

        return self.report.to_dict()

    def restart(self) -> dict:
        """Restart cloud monitoring."""

        self.stop()

        return self.start()
