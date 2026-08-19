from typing import Any, Dict

from ..base import IntegrationProvider


class GenericWebProvider(IntegrationProvider):
    """Generic web/API integration adapter."""

    name = "GENERIC_WEB"
    category = "WEB_API"

    def health(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "category": self.category,
            "status": "READY",
            "authentication": "NOT_CONFIGURED",
            "connection": "NOT_CONNECTED",
        }
