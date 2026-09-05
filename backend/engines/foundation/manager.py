"""
MAIN BASE FOUNDATION
Foundation Engine

Connects the central foundation systems with
the MAIN-BASE-FOUNDATION EngineManager.
"""

from pathlib import Path

from foundation.core.bootstrap import FoundationBootstrap


class FoundationEngine:
    """
    Central foundation engine.

    Provides the lifecycle interface required by
    EngineManager.
    """

    def __init__(self):
        self.status = "STOPPED"

        self.root = Path(
            __file__
        ).resolve().parents[3]

        self.bootstrap = None

    def start(self):
        """
        Start the central foundation system.
        """

        self.bootstrap = FoundationBootstrap(
            str(self.root)
        )

        self.status = "RUNNING"

        return self.status

    def stop(self):
        """
        Stop the central foundation system.
        """

        self.bootstrap = None
        self.status = "STOPPED"

        return self.status

    def restart(self):
        """
        Restart the foundation system.
        """

        self.stop()
        return self.start()

    def system_status(self) -> dict:
        """
        Return the complete foundation status.
        """

        if self.bootstrap is None:
            return {
                "status": self.status
            }

        return self.bootstrap.status()


__all__ = [
    "FoundationEngine",
]
