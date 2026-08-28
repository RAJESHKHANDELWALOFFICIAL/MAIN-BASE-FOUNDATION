from abc import ABC, abstractmethod
from typing import Any, Dict


class IntegrationProvider(ABC):
    """Universal integration provider contract."""

    name: str = "UNKNOWN"
    category: str = "GENERAL"

    @abstractmethod
    def health(self) -> Dict[str, Any]:
        """Return provider health information."""
        raise NotImplementedError

    def metadata(self) -> Dict[str, Any]:
        """Return provider metadata."""

        return {
            "name": self.name,
            "category": self.category,
        }
