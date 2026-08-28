from typing import Dict, List

from .models import CloudProviderStatus


class CloudProviderRegistry:
    """Registry of supported global cloud providers."""

    def __init__(self):
        self.providers: Dict[str, CloudProviderStatus] = {}

        self.register(
            CloudProviderStatus(
                provider="AWS",
                category="CLOUD_INFRASTRUCTURE",
                capabilities=[
                    "COMPUTE",
                    "STORAGE",
                    "DATABASE",
                    "NETWORKING",
                    "SECURITY",
                    "MONITORING",
                ],
                status="READY_FOR_AUTHORIZATION",
                message=(
                    "AWS integration is ready for authorized "
                    "credential configuration."
                ),
            )
        )

        self.register(
            CloudProviderStatus(
                provider="GOOGLE_CLOUD",
                category="CLOUD_INFRASTRUCTURE",
                capabilities=[
                    "COMPUTE",
                    "STORAGE",
                    "DATABASE",
                    "NETWORKING",
                    "AI",
                    "SECURITY",
                    "MONITORING",
                ],
                status="READY_FOR_AUTHORIZATION",
                message=(
                    "Google Cloud integration is ready for "
                    "authorized credential configuration."
                ),
            )
        )

        self.register(
            CloudProviderStatus(
                provider="MICROSOFT_AZURE",
                category="CLOUD_INFRASTRUCTURE",
                capabilities=[
                    "COMPUTE",
                    "STORAGE",
                    "DATABASE",
                    "NETWORKING",
                    "IDENTITY",
                    "SECURITY",
                    "MONITORING",
                ],
                status="READY_FOR_AUTHORIZATION",
                message=(
                    "Microsoft Azure integration is ready for "
                    "authorized credential configuration."
                ),
            )
        )

        self.register(
            CloudProviderStatus(
                provider="CLOUDFLARE",
                category="EDGE_CLOUD",
                capabilities=[
                    "DNS",
                    "CDN",
                    "EDGE",
                    "SECURITY",
                    "WORKERS",
                    "NETWORKING",
                ],
                status="READY_FOR_AUTHORIZATION",
                message=(
                    "Cloudflare integration is ready for "
                    "authorized credential configuration."
                ),
            )
        )

    def register(
        self,
        provider: CloudProviderStatus,
    ) -> None:
        """Register a cloud provider."""

        self.providers[
            provider.provider.upper()
        ] = provider

    def get(
        self,
        provider: str,
    ) -> CloudProviderStatus:
        """Return one registered provider."""

        key = provider.strip().upper()

        if key not in self.providers:
            raise KeyError(
                f"Unsupported cloud provider: {provider}"
            )

        return self.providers[key]

    def list(self) -> List[CloudProviderStatus]:
        """Return all registered cloud providers."""

        return list(self.providers.values())

    def names(self) -> List[str]:
        """Return registered provider names."""

        return list(self.providers.keys())

    def statuses(self) -> List[dict]:
        """Return provider status information."""

        return [
            provider.to_dict()
            for provider in self.providers.values()
        ]

    def exists(
        self,
        provider: str,
    ) -> bool:
        """Check whether a provider is registered."""

        return provider.strip().upper() in self.providers
