"""
MAIN BASE FOUNDATION
Central Bootstrap

Initializes and connects the core foundation
subsystems into one operational system.
"""

from pathlib import Path

from foundation.core.foundation import foundation
from foundation.core.orchestrator import orchestrator

from foundation.file_manager.manager import FileManager
from foundation.sync.sync import SyncEngine


class FoundationBootstrap:
    """
    Creates the central runtime configuration for
    MAIN-BASE-FOUNDATION.
    """

    def __init__(self, root: str):
        self.root = Path(root).resolve()

        self.file_manager = FileManager(
            str(self.root)
        )

        self.sync_engine = SyncEngine(
            str(self.root)
        )

        orchestrator.set_file_manager(
            self.file_manager
        )

        orchestrator.set_sync_engine(
            self.sync_engine
        )

    def status(self) -> dict:
        """
        Return complete foundation status.
        """

        return {
            "foundation": foundation.info(),
            "systems": orchestrator.status(),
            "root": str(self.root),
        }

    def synchronize(self) -> dict:
        """
        Synchronize filesystem and registry.
        """

        return orchestrator.synchronize()


__all__ = [
    "FoundationBootstrap",
]
