from typing import Any, Dict

from .registry import IntegrationRegistry


class IntegrationHealth:
    """Global integration health service."""

    def __init__(self):
        self.registry = IntegrationRegistry()

    def status(self) -> Dict[str, Any]:
        providers = self.registry.health()

        return {
            "system": "MAIN BASE FOUNDATION",
            "integration_count": len(providers),
            "ready_count": sum(
                1
                for provider in providers
                if provider["status"] == "READY"
            ),
            "providers": providers,
        }
