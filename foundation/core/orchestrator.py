"""
MAIN BASE FOUNDATION
Central Integration and Orchestration Layer

Coordinates the Foundation Core, Identity, Registry,
File Manager, Synchronization, Security, Dependencies,
Audit and Integrity systems.
"""

from foundation.audit.audit import audit_log
from foundation.core.integrity import integrity
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

    # ==========================================================
    # CONNECTIONS
    # ==========================================================

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

    # ==========================================================
    # STATUS
    # ==========================================================

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
            "integrity": "active",
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

    # ==========================================================
    # IDENTITY
    # ==========================================================

    def register_identity(
        self,
        identity,
    ):
        return identity_manager.register(
            identity
        )

    def get_identity(
        self,
        entity_id: str,
    ):
        return identity_manager.get(
            entity_id
        )

    def update_identity(
        self,
        entity_id: str,
        **changes,
    ):
        return identity_manager.update(
            entity_id,
            **changes,
        )

    # ==========================================================
    # REGISTRY
    # ==========================================================

    def register_entity(
        self,
        entry,
    ):
        return registry.register(
            entry
        )

    def get_entity(
        self,
        entity_id: str,
    ):
        return registry.require(
            entity_id
        )

    def list_entities(self) -> list[dict]:
        return registry.list_all()

    # ==========================================================
    # DEPENDENCIES
    # ==========================================================

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

    def get_dependencies(
        self,
        source_id: str,
    ):
        return dependency_index.get_dependencies(
            source_id
        )

    def get_dependents(
        self,
        target_id: str,
    ):
        return dependency_index.get_dependents(
            target_id
        )

    def get_relationships(
        self,
        entity_id: str,
    ):
        return dependency_index.get_entity_relationships(
            entity_id
        )

    # ==========================================================
    # SECURITY
    # ==========================================================

    def set_permissions(
        self,
        subject_id: str,
        operations,
    ) -> None:
        access_controller.set_permissions(
            subject_id,
            operations,
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

    # ==========================================================
    # AUDIT
    # ==========================================================

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

    # ==========================================================
    # INTEGRITY
    # ==========================================================

    def integrity_check(self) -> dict:
        """
        Run the central Foundation integrity check.
        """

        return integrity.check()

    def registry_integrity(self) -> dict:
        return integrity.registry_check()

    def dependency_integrity(self) -> dict:
        return integrity.dependency_check()

    # ==========================================================
    # SYNCHRONIZATION
    # ==========================================================

    def synchronize(self) -> dict:
        """
        Synchronize the filesystem with the registry
        and then return the resulting integrity state.
        """

        if self.sync_engine is None:
            raise RuntimeError(
                "Sync engine is not connected."
            )

        synchronization = (
            self.sync_engine.synchronize()
        )

        integrity_result = (
            self.integrity_check()
        )

        return {
            "synchronization": synchronization,
            "integrity": integrity_result,
        }


orchestrator = FoundationOrchestrator()


__all__ = [
    "FoundationOrchestrator",
    "orchestrator",
]
