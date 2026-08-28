"""Global integration data models."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class IntegrationStatus:
    provider: str
    category: str
    configured: bool = False
    authenticated: bool = False
    available: bool = False
    status: str = "NOT_CONFIGURED"
    message: str = ""
    capabilities: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "provider": self.provider,
            "category": self.category,
            "configured": self.configured,
            "authenticated": self.authenticated,
            "available": self.available,
            "status": self.status,
            "message": self.message,
            "capabilities": self.capabilities,
        }


@dataclass
class IntegrationDefinition:
    provider: str
    category: str
    official_api: str
    authentication: str
    capabilities: List[str] = field(default_factory=list)
    requires_credentials: bool = True

    def to_dict(self) -> dict:
        return {
            "provider": self.provider,
            "category": self.category,
            "official_api": self.official_api,
            "authentication": self.authentication,
            "capabilities": self.capabilities,
            "requires_credentials": self.requires_credentials,
        }
