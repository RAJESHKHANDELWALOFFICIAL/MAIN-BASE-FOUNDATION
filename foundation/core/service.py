"""
MAIN BASE FOUNDATION
Central Foundation Service

Single operational entry point for the complete
MAIN-BASE-FOUNDATION foundation layer.
"""

from foundation.core.orchestrator import orchestrator


class FoundationService:
    """
    Public service facade for the complete Foundation.

    All major Foundation systems are exposed through
    the central Orchestrator instead of duplicating
    system-level coordination logic here.
    """

    def __init__(
        self,
        file_manager=None,
        sync_engine=None,
    ):
        self.file_manager = file_manager
        self.sync_engine = sync_engine

        if file_manager is not None:
            orchestrator.set_file_manager(file_manager)

        if sync_engine is not None:
            orchestrator.set_sync_engine(sync_engine)

    # ==========================================================
    # CONNECTIONS
    # ==========================================================

    def set_file_manager(self, file_manager):
        self.file_manager = file_manager
        orchestrator.set_file_manager(file_manager)

    def set_sync_engine(self, sync_engine):
        self.sync_engine = sync_engine
        orchestrator.set_sync_engine(sync_engine)

    # ==========================================================
    # FILE OPERATIONS
    # ==========================================================

    def _require_file_manager(self):
        if self.file_manager is None:
            raise RuntimeError(
                "File Manager is not connected."
            )

        return self.file_manager

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
        return orchestrator.register_identity(
            identity
        )

    def get_identity(
        self,
        entity_id,
    ):
        return orchestrator.get_identity(
            entity_id
        )

    def get_identity_representation(
        self,
        entity_id,
        identity_type,
    ):
        identity = self.get_identity(entity_id)

        if identity is None:
            return None

        representations = {
            "small": identity.small,
            "capital": identity.capital,
            "bold": identity.bold,
            "icon_emoji": identity.icon_emoji,
        }

        if identity_type not in representations:
            raise ValueError(
                "Unknown identity representation: "
                f"{identity_type}"
            )

        return representations[identity_type]

    def update_identity(
        self,
        entity_id,
        **changes,
    ):
        return orchestrator.update_identity(
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
        return orchestrator.register_entity(
            entry
        )

    def get_entity(
        self,
        entity_id,
    ):
        return orchestrator.get_entity(
            entity_id
        )

    def list_entities(self):
        return orchestrator.list_entities()

    # ==========================================================
    # DEPENDENCIES
    # ==========================================================

    def add_dependency(
        self,
        source_id,
        target_id,
        relationship,
    ):
        return orchestrator.add_dependency(
            source_id=source_id,
            target_id=target_id,
            relationship=relationship,
        )

    def get_dependencies(
        self,
        entity_id,
    ):
        return orchestrator.get_dependencies(
            entity_id
        )

    def get_dependents(
        self,
        entity_id,
    ):
        return orchestrator.get_dependents(
            entity_id
        )

    def get_relationships(
        self,
        entity_id,
    ):
        return orchestrator.get_relationships(
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
        return orchestrator.set_permissions(
            subject_id,
            operations,
        )

    def authorize(
        self,
        subject_id,
        operation,
        path,
    ):
        return orchestrator.authorize(
            subject_id=subject_id,
            operation=operation,
            path=path,
        )

    # ==========================================================
    # AUDIT
    # ==========================================================

    def audit(
        self,
        operation,
        entity_id,
        path,
        subject_id,
        status,
        details="",
    ):
        return orchestrator.audit(
            operation=operation,
            entity_id=entity_id,
            path=path,
            subject_id=subject_id,
            status=status,
            details=details,
        )

    def audit_history(
        self,
        entity_id,
    ):
        from foundation.audit.audit import audit_log

        return audit_log.get_entity_history(
            entity_id
        )

    def subject_history(
        self,
        subject_id,
    ):
        from foundation.audit.audit import audit_log

        return audit_log.get_subject_history(
            subject_id
        )

    # ==========================================================
    # INTEGRITY
    # ==========================================================

    def integrity_check(self):
        return orchestrator.integrity_check()

    def registry_integrity(self):
        return orchestrator.registry_integrity()

    def dependency_integrity(self):
        return orchestrator.dependency_integrity()

    # ==========================================================
    # SYNCHRONIZATION
    # ==========================================================

    def synchronize(self):
        if self.sync_engine is None:
            raise RuntimeError(
                "Sync Engine is not connected."
            )

        return orchestrator.synchronize()

    # ==========================================================
    # SYSTEM STATUS
    # ==========================================================

    def status(self) -> dict:
        return orchestrator.status()


__all__ = [
    "FoundationService",
]
