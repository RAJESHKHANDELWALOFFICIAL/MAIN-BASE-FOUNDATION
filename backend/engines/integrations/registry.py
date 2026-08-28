"""Global integration registry."""

from typing import Dict, List

from .models import IntegrationDefinition, IntegrationStatus


class IntegrationRegistry:
    """Central registry for authorized external integrations."""

    def __init__(self):
        self.definitions: Dict[str, IntegrationDefinition] = {}

        self.register(
            IntegrationDefinition(
                provider="GOOGLE",
                category="CLOUD_IDENTITY_SERVICES",
                official_api="Google APIs",
                authentication="OAUTH2",
                capabilities=[
                    "IDENTITY",
                    "CLOUD",
                    "DRIVE",
                    "GMAIL",
                    "CALENDAR",
                    "MAPS",
                    "YOUTUBE",
                ],
            )
        )

        self.register(
            IntegrationDefinition(
                provider="MICROSOFT",
                category="CLOUD_IDENTITY_SERVICES",
                official_api="Microsoft Graph / Azure APIs",
                authentication="OAUTH2_OIDC",
                capabilities=[
                    "IDENTITY",
                    "GRAPH",
                    "OUTLOOK",
                    "ONEDRIVE",
                    "SHAREPOINT",
                    "TEAMS",
                    "AZURE",
                ],
            )
        )

        self.register(
            IntegrationDefinition(
                provider="AWS",
                category="CLOUD_INFRASTRUCTURE",
                official_api="AWS APIs / SDK",
                authentication="IAM",
                capabilities=[
                    "CLOUD",
                    "COMPUTE",
                    "STORAGE",
                    "DATABASE",
                    "NETWORKING",
                    "MONITORING",
                ],
            )
        )

        self.register(
            IntegrationDefinition(
                provider="APPLE",
                category="IDENTITY_DEVICE_SERVICES",
                official_api="Apple Developer APIs",
                authentication="OAUTH2_OIDC",
                capabilities=[
                    "IDENTITY",
                    "IOS",
                    "IPADOS",
                    "MACOS",
                ],
            )
        )

        self.register(
            IntegrationDefinition(
                provider="GITHUB",
                category="DEVELOPER_PLATFORM",
                official_api="GitHub REST / GraphQL APIs",
                authentication="OAUTH2_TOKEN",
                capabilities=[
                    "REPOSITORIES",
                    "ISSUES",
                    "PULL_REQUESTS",
                    "ACTIONS",
                    "RELEASES",
                ],
            )
        )

        self.register(
            IntegrationDefinition(
                provider="CLOUDFLARE",
                category="EDGE_INFRASTRUCTURE",
                official_api="Cloudflare APIs",
                authentication="API_TOKEN",
                capabilities=[
                    "DNS",
                    "CDN",
                    "EDGE",
                    "SECURITY",
                    "WORKERS",
                ],
            )
        )

    def register(
        self,
        definition: IntegrationDefinition,
    ) -> None:
        self.definitions[definition.provider] = definition

    def list(self) -> List[dict]:
        return [
            definition.to_dict()
            for definition in self.definitions.values()
        ]

    def get(
        self,
        provider: str,
    ) -> IntegrationDefinition:
        return self.definitions[provider.upper()]

    def status(
        self,
        provider: str,
    ) -> IntegrationStatus:
        definition = self.get(provider)

        return IntegrationStatus(
            provider=definition.provider,
            category=definition.category,
            configured=False,
            authenticated=False,
            available=True,
            status="READY_FOR_AUTHORIZATION",
            message=(
                "Provider adapter is registered. "
                "Credentials and explicit authorization are required."
            ),
            capabilities=definition.capabilities,
        )

    def statuses(self) -> List[dict]:
        return [
            self.status(provider).to_dict()
            for provider in self.definitions
        ]
