from typing import Any, Dict, List

from .providers.aws import AWSProvider
from .providers.google import GoogleProvider
from .providers.microsoft import MicrosoftProvider
from .providers.generic import GenericWebProvider


class IntegrationRegistry:
    """Central registry for global integrations."""

    def __init__(self):
        self.providers = {
            "GOOGLE": GoogleProvider(),
            "MICROSOFT": MicrosoftProvider(),
            "AWS": AWSProvider(),
            "GENERIC_WEB": GenericWebProvider(),
        }

    def list(self) -> List[Dict[str, Any]]:
        return [
            provider.metadata()
            for provider in self.providers.values()
        ]

    def health(self) -> List[Dict[str, Any]]:
        return [
            provider.health()
            for provider in self.providers.values()
        ]

    def get(self, name: str):
        return self.providers.get(name.upper())
