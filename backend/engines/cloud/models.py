from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class CloudServiceStatus:
    """Status of one cloud service."""

    name: str
    provider: str
    region: Optional[str] = None

    available: bool = False
    online: bool = False

    latency_ms: Optional[float] = None

    status: str = "UNKNOWN"
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "provider": self.provider,
            "region": self.region,
            "available": self.available,
            "online": self.online,
            "latency_ms": self.latency_ms,
            "status": self.status,
            "error": self.error,
        }


@dataclass
class CloudProviderStatus:
    """Unified cloud provider status."""

    provider: str
    category: str

    configured: bool = False
    authenticated: bool = False

    available: bool = False
    online: bool = False

    status: str = "NOT_CONFIGURED"

    region: Optional[str] = None

    services: List[CloudServiceStatus] = field(
        default_factory=list
    )

    capabilities: List[str] = field(
        default_factory=list
    )

    message: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "provider": self.provider,
            "category": self.category,
            "configured": self.configured,
            "authenticated": self.authenticated,
            "available": self.available,
            "online": self.online,
            "status": self.status,
            "region": self.region,
            "services": [
                service.to_dict()
                for service in self.services
            ],
            "capabilities": self.capabilities,
            "message": self.message,
        }


@dataclass
class CloudHealthReport:
    """Unified cloud infrastructure health report."""

    healthy: bool = False
    status: str = "UNKNOWN"

    total_providers: int = 0
    configured_providers: int = 0
    authenticated_providers: int = 0
    online_providers: int = 0

    providers: List[CloudProviderStatus] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )

    last_check: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "healthy": self.healthy,
            "status": self.status,
            "total_providers": self.total_providers,
            "configured_providers": self.configured_providers,
            "authenticated_providers": (
                self.authenticated_providers
            ),
            "online_providers": self.online_providers,
            "providers": [
                provider.to_dict()
                for provider in self.providers
            ],
            "warnings": self.warnings,
            "last_check": self.last_check,
        }


@dataclass
class CloudReport:
    """MAIN BASE FOUNDATION unified cloud report."""

    providers: List[CloudProviderStatus] = field(
        default_factory=list
    )

    health: CloudHealthReport = field(
        default_factory=CloudHealthReport
    )

    online: bool = False
    offline: bool = True

    status: str = "UNKNOWN"

    reason: Optional[str] = None

    capabilities: Dict[str, bool] = field(
        default_factory=dict
    )

    last_check: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "providers": [
                provider.to_dict()
                for provider in self.providers
            ],
            "health": self.health.to_dict(),
            "online": self.online,
            "offline": self.offline,
            "status": self.status,
            "reason": self.reason,
            "capabilities": self.capabilities,
            "last_check": self.last_check,
        }
