from typing import Any, Dict, List

from .providers.aws import AWSProvider
from .providers.google import GoogleProvider
from .providers.microsoft import MicrosoftProvider
from .providers.apple import AppleProvider
from .providers.generic import GenericWebProvider


class IntegrationRegistry:
    """Central registry for global integrations."""

    def __init__(self):
        self.providers = {
            "GOOGLE": GoogleProvider(),
            "MICROSOFT": MicrosoftProvider(),
            "AWS": AWSProvider(),
            "APPLE": AppleProvider(),
            "GENERIC_WEB": GenericWebProvider(),
        }

    def list(self) -> List[Dict[str, Any]]:
        """Return metadata for all registered providers."""

        return [
            provider.metadata()
            for provider in self.providers.values()
        ]

    def health(self) -> List[Dict[str, Any]]:
        """Return health information for all providers."""

        return [
            provider.health()
            for provider in self.providers.values()
        ]

    def get(
        self,
        name: str,
    ) -> Any:
        """Return a provider by name."""

        if not isinstance(name, str):
            raise TypeError(
                "Provider name must be a string."
            )

        return self.providers.get(
            name.upper()
        )


__all__ = [
    "IntegrationRegistry",
]
