from typing import Any, Dict

from ..base import IntegrationProvider


class MicrosoftProvider(IntegrationProvider):
    """Microsoft ecosystem integration adapter."""

    name = "MICROSOFT"
    category = "CLOUD_PLATFORM"

    def health(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "category": self.category,
            "status": "READY",
            "authentication": "NOT_CONFIGURED",
            "connection": "NOT_CONNECTED",
        }
