"""
MAIN BASE FOUNDATION
Central Foundation Bootstrap

Controls the complete lifecycle of the Foundation layer.
"""

from pathlib import Path

from foundation.core.foundation import foundation
from foundation.core.integrity import integrity
from foundation.core.orchestrator import orchestrator
from foundation.core.service import FoundationService

from foundation.file_manager.manager import FileManager
from foundation.sync.sync import SyncEngine


class FoundationBootstrap:
    """
    Central lifecycle controller for the Foundation.
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

        self.service = FoundationService(
            file_manager=self.file_manager,
            sync_engine=self.sync_engine,
        )

        self.started = False

    # ==========================================================
    # START
    # ==========================================================

    def start(self) -> dict:
        """
        Start the complete Foundation lifecycle.
        """

        if self.started:
            return self.status()

        foundation.status = "active"

        self.started = True

        return self.status()

    # ==========================================================
    # SYNCHRONIZE
    # ==========================================================

    def synchronize(self) -> dict:
        """
        Synchronize the filesystem and validate integrity.
        """

        if not self.started:
            self.start()

        return self.service.synchronize()

    # ==========================================================
    # INTEGRITY
    # ==========================================================

    def integrity_check(self) -> dict:
        """
        Run a complete Foundation integrity check.
        """

        return integrity.check(
            root=self.root
        )

    # ==========================================================
    # STATUS
    # ==========================================================

    def status(self) -> dict:
        """
        Return complete Foundation lifecycle status.
        """

        return {
            "foundation": foundation.info(),
            "lifecycle": (
                "RUNNING"
                if self.started
                else "STOPPED"
            ),
            "systems": orchestrator.status(),
            "service": self.service.status(),
            "integrity": self.integrity_check(),
            "root": str(self.root),
        }

    # ==========================================================
    # STOP
    # ==========================================================

    def stop(self) -> dict:
        """
        Stop the Foundation lifecycle controller.
        """

        self.started = False

        return {
            "foundation": foundation.info(),
            "lifecycle": "STOPPED",
            "root": str(self.root),
        }


__all__ = [
    "FoundationBootstrap",
]
