"""
MAIN BASE FOUNDATION
Central Integration and Orchestration Layer

Coordinates the Foundation Core, Identity, Registry,
File Manager, Synchronization, Security and Audit systems.
"""

from foundation.audit.audit import audit_log
from foundation.dependencies.index import dependency_index
from foundation.identity.identity import identity_manager
from foundation.registry.registry import registry
from foundation.security.access import access_controller


class FoundationOrchestrator:
    """
    Central coordinator for MAIN-BASE-FOUNDATION systems.
    """

    def __init__(
        self,
        file_manager=None,
        sync_engine=None,
    ):
        self.file_manager = file_manager
        self.sync_engine = sync_engine

    def set_file_manager(
        self,
        file_manager,
    ) -> None:
        self.file_manager = file_manager

    def set_sync_engine(
        self,
        sync_engine,
    ) -> None:
        self.sync_engine = sync_engine

    def status(self) -> dict:
        """
        Return the current status of all
        connected foundation subsystems.
        """

        return {
            "foundation": "active",
            "identity": "active",
            "registry": "active",
            "dependencies": "active",
            "security": "active",
            "audit": "active",
            "file_manager": (
                "connected"
                if self.file_manager is not None
                else "not_connected"
            ),
            "sync_engine": (
                "connected"
                if self.sync_engine is not None
                else "not_connected"
            ),
        }

    def register_identity(
        self,
        identity,
    ):
        return identity_manager.register(
            identity
        )

    def register_entity(
        self,
        entry,
    ):
        return registry.register(
            entry
        )

    def add_dependency(
        self,
        source_id: str,
        target_id: str,
        relationship: str,
    ):
        return dependency_index.add(
            source_id=source_id,
            target_id=target_id,
            relationship=relationship,
        )

    def authorize(
        self,
        subject_id: str,
        operation: str,
        path: str,
    ) -> None:
        access_controller.authorize_path(
            subject_id=subject_id,
            operation=operation,
            path=path,
        )

    def audit(
        self,
        operation: str,
        entity_id: str,
        path: str,
        subject_id: str,
        status: str,
        details: str = "",
    ):
        return audit_log.record(
            operation=operation,
            entity_id=entity_id,
            path=path,
            subject_id=subject_id,
            status=status,
            details=details,
        )

    def synchronize(self) -> dict:
        """
        Synchronize the filesystem with the registry.
        """

        if self.sync_engine is None:
            raise RuntimeError(
                "Sync engine is not connected."
            )

        return self.sync_engine.synchronize()


orchestrator = FoundationOrchestrator()


__all__ = [
    "FoundationOrchestrator",
    "orchestrator",
]
