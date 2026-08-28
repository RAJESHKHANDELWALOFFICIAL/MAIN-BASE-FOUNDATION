from abc import ABC, abstractmethod
from typing import Dict


class ConnectivityPlatform(ABC):
    """Base interface for platform-specific connectivity adapters."""

    platform_name = "UNKNOWN"

    @abstractmethod
    def capabilities(self) -> Dict[str, bool]:
        """Return capabilities supported by the platform."""

        raise NotImplementedError

    @abstractmethod
    def connectivity(self) -> Dict[str, object]:
        """Return platform connectivity information."""

        raise NotImplementedError

    @abstractmethod
    def scan_networks(self) -> list:
        """Return safely discoverable networks."""

        raise NotImplementedError
