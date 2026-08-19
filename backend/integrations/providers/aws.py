from typing import Any, Dict

from ..base import IntegrationProvider


class AWSProvider(IntegrationProvider):
    """AWS integration adapter."""

    name = "AWS"
    category = "CLOUD_PLATFORM"

    def health(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "category": self.category,
            "status": "READY",
            "authentication": "NOT_CONFIGURED",
            "connection": "NOT_CONNECTED",
        }
