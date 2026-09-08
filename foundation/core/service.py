"""
MAIN BASE FOUNDATION
Central Foundation Service

Single operational entry point for the complete
MAIN-BASE-FOUNDATION foundation layer.
"""

from foundation.audit.audit import audit_log
from foundation.dependencies.index import dependency_index
from foundation.identity.identity import identity_manager
from foundation.registry.registry import registry
from foundation.security.access import access_controller


class FoundationService:
    """
    Central service facade for Foundation operations.

    This layer does not replace the underlying systems.
    It coordinates them through one controlled interface.
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

    def set_file_manager(self, file_manager):
        self.file_manager = file_manager

    def set_sync_engine(self, sync_engine):
        self.sync_engine = sync_engine

    def _require_file_manager(self):
        if self.file_manager is None:
            raise RuntimeError(
                "File Manager is not connected."
            )

        return self.file_manager

    def _require_sync_engine(self):
        if self.sync_engine is None:
            raise RuntimeError(
                "Sync Engine is not connected."
            )

        return self.sync_engine

    # ==========================================================
    # FILE OPERATIONS
    # ==========================================================

    def create_file(
        self,
        path,
        entity_id,
        identity_id,
        subject_id,
        content="",
    ):
        return self._require_file_manager().create_file(
            path=path,
            entity_id=entity_id,
            identity_id=identity_id,
            subject_id=subject_id,
            content=content,
        )

    def create_folder(
        self,
        path,
        entity_id,
        identity_id,
        subject_id,
    ):
        return self._require_file_manager().create_folder(
            path=path,
            entity_id=entity_id,
            identity_id=identity_id,
            subject_id=subject_id,
        )

    def read_file(
        self,
        path,
        subject_id,
    ):
        return self._require_file_manager().read_file(
            path=path,
            subject_id=subject_id,
        )

    def search(
        self,
        query,
        subject_id,
        path=".",
    ):
        return self._require_file_manager().search(
            query=query,
            subject_id=subject_id,
            path=path,
        )

    def rename(
        self,
        entity_id,
        destination,
        subject_id,
    ):
        return self._require_file_manager().rename(
            entity_id=entity_id,
            destination=destination,
            subject_id=subject_id,
        )

    def move(
        self,
        entity_id,
        destination,
        subject_id,
    ):
        return self._require_file_manager().move(
            entity_id=entity_id,
            destination=destination,
            subject_id=subject_id,
        )

    def copy(
        self,
        source_entity_id,
        destination,
        entity_id,
        identity_id,
        subject_id,
    ):
        return self._require_file_manager().copy(
            source_entity_id=source_entity_id,
            destination=destination,
            entity_id=entity_id,
            identity_id=identity_id,
            subject_id=subject_id,
        )

    def delete(
        self,
        entity_id,
        subject_id,
    ):
        return self._require_file_manager().delete(
            entity_id=entity_id,
            subject_id=subject_id,
        )

    def list_directory(
        self,
        path=".",
        subject_id="",
    ):
        return self._require_file_manager().list_directory(
            path=path,
            subject_id=subject_id,
        )

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
        entity_id,
    ):
        return identity_manager.require(
            entity_id
        )

    def get_identity_representation(
        self,
        entity_id,
        identity_type,
    ):
        return identity_manager.get_representation(
            entity_id,
            identity_type,
        )

    def update_identity(
        self,
        entity_id,
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
        entity_id,
    ):
        return registry.require(
            entity_id
        )

    def list_entities(self):
        return registry.list_all()

    # ==========================================================
    # DEPENDENCIES
    # ==========================================================

    def add_dependency(
        self,
        source_id,
        target_id,
        relationship,
    ):
        return dependency_index.add(
            source_id=source_id,
            target_id=target_id,
            relationship=relationship,
        )

    def get_dependencies(
        self,
        entity_id,
    ):
        return dependency_index.get_dependencies(
            entity_id
        )

    def get_dependents(
        self,
        entity_id,
    ):
        return dependency_index.get_dependents(
            entity_id
        )

    def get_relationships(
        self,
        entity_id,
    ):
        return dependency_index.get_entity_relationships(
            entity_id
        )

    # ==========================================================
    # SECURITY
    # ==========================================================

    def set_permissions(
        self,
        subject_id,
        operations,
    ):
        return access_controller.set_permissions(
            subject_id,
            operations,
        )

    def authorize(
        self,
        subject_id,
        operation,
        path,
    ):
        return access_controller.authorize_path(
            subject_id=subject_id,
            operation=operation,
            path=path,
        )

    # ==========================================================
    # AUDIT
    # ==========================================================

    def audit_history(
        self,
        entity_id,
    ):
        return audit_log.get_entity_history(
            entity_id
        )

    def subject_history(
        self,
        subject_id,
    ):
        return audit_log.get_subject_history(
            subject_id
        )

    # ==========================================================
    # SYNCHRONIZATION
    # ==========================================================

    def synchronize(self):
        return self._require_sync_engine().synchronize()

    # ==========================================================
    # SYSTEM STATUS
    # ==========================================================

    def status(self) -> dict:
        return {
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
            "identity": "active",
            "registry": "active",
            "dependencies": "active",
            "security": "active",
            "audit": "active",
        }


__all__ = [
    "FoundationService",
]
