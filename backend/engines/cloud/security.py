from typing import List

from .models import CloudProviderStatus


class CloudSecurityMonitor:
    """Security assessment for cloud provider integrations."""

    def assess(
        self,
        providers: List[CloudProviderStatus],
    ) -> dict:
        """Assess cloud integration security."""

        warnings: List[str] = []
        checks: List[dict] = []

        for provider in providers:
            if not provider.configured:
                checks.append(
                    {
                        "provider": provider.provider,
                        "check": "configuration",
                        "status": "NOT_CONFIGURED",
                    }
                )

                continue

            if provider.authenticated:
                checks.append(
                    {
                        "provider": provider.provider,
                        "check": "authentication",
                        "status": "AUTHENTICATED",
                    }
                )
            else:
                checks.append(
                    {
                        "provider": provider.provider,
                        "check": "authentication",
                        "status": "NOT_AUTHENTICATED",
                    }
                )

                warnings.append(
                    f"{provider.provider}: "
                    "provider authentication is unavailable."
                )

        if not providers:
            overall = "UNKNOWN"

        elif warnings:
            overall = "WARNING"

        else:
            overall = "SECURE"

        return {
            "security": overall,
            "warnings": warnings,
            "checks": checks,
        }

    def provider_security(
        self,
        provider: CloudProviderStatus,
    ) -> dict:
        """Return security information for one provider."""

        if not provider.configured:
            status = "NOT_CONFIGURED"

        elif provider.authenticated:
            status = "AUTHENTICATED"

        else:
            status = "NOT_AUTHENTICATED"

        return {
            "provider": provider.provider,
            "configured": provider.configured,
            "authenticated": provider.authenticated,
            "security": status,
        }
