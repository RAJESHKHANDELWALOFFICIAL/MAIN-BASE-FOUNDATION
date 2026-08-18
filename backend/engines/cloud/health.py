from datetime import datetime, timezone
from typing import List

from .models import (
    CloudHealthReport,
    CloudProviderStatus,
)


class CloudHealthMonitor:
    """Unified health assessment for registered cloud providers."""

    def assess(
        self,
        providers: List[CloudProviderStatus],
    ) -> CloudHealthReport:
        """Assess the current health of cloud providers."""

        total = len(providers)
        configured = 0
        authenticated = 0
        online = 0

        warnings: List[str] = []

        for provider in providers:
            if provider.configured:
                configured += 1

            if provider.authenticated:
                authenticated += 1

            if provider.online:
                online += 1

            if provider.status not in {
                "ONLINE",
                "READY_FOR_AUTHORIZATION",
            }:
                if provider.message:
                    warnings.append(
                        f"{provider.provider}: "
                        f"{provider.message}"
                    )

        if total == 0:
            status = "UNKNOWN"
            healthy = False

        elif online > 0:
            status = "HEALTHY"
            healthy = True

        elif configured == 0:
            status = "NOT_CONFIGURED"
            healthy = False

        else:
            status = "WARNING"
            healthy = False

        return CloudHealthReport(
            healthy=healthy,
            status=status,
            total_providers=total,
            configured_providers=configured,
            authenticated_providers=authenticated,
            online_providers=online,
            providers=providers,
            warnings=warnings,
            last_check=datetime.now(
                timezone.utc
            ).isoformat(),
        )

    def provider_health(
        self,
        provider: CloudProviderStatus,
    ) -> dict:
        """Return health information for one provider."""

        return {
            "provider": provider.provider,
            "configured": provider.configured,
            "authenticated": provider.authenticated,
            "available": provider.available,
            "online": provider.online,
            "status": provider.status,
            "message": provider.message,
        }
