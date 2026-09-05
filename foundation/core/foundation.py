"""
MAIN BASE FOUNDATION
Foundation Core

Central core identity and metadata for the
entire MAIN-BASE-FOUNDATION system.
"""


class Foundation:
    """
    Central representation of MAIN-BASE-FOUNDATION.
    """

    SYSTEM_NAME = "MAIN-BASE-FOUNDATION"
    SYSTEM_VERSION = "1.0.0"

    def __init__(self):
        self.name = self.SYSTEM_NAME
        self.version = self.SYSTEM_VERSION
        self.status = "active"

    def info(self) -> dict:
        """
        Return the current foundation information.
        """

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status,
        }

    def is_active(self) -> bool:
        """
        Check whether the foundation is active.
        """

        return self.status == "active"


foundation = Foundation()


__all__ = [
    "Foundation",
    "foundation",
]
