from typing import Any, Dict

from ..base import IntegrationProvider


class GoogleProvider(IntegrationProvider):
    """Google ecosystem integration adapter."""

    name = "GOOGLE"
    category = "CLOUD_PLATFORM"

    def health(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "category": self.category,
            "status": "READY",
            "authentication": "NOT_CONFIGURED",
            "connection": "NOT_CONNECTED",
        }
