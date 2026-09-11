"""
MAIN BASE FOUNDATION
Foundation Integrity Layer

Central consistency checks for Registry, Identity,
Dependencies and Filesystem.
"""

from pathlib import Path

from foundation.dependencies.index import dependency_index
from foundation.identity.identity import identity_manager
from foundation.registry.registry import registry


class FoundationIntegrity:
    """
    Central consistency checker for the Foundation layer.
    """

    # ==========================================================
    # REGISTRY CHECK
    # ==========================================================

    def registry_check(self) -> dict:
        """
        Check registry entries for structural validity,
        duplicate paths and filesystem consistency.
        """

        entries = registry.list_all()

        invalid = []
        paths = {}

        for entry in entries:

            entity_id = entry.get("entity_id")
            path = entry.get("path")
            identity_id = entry.get("identity_id")

            if not entity_id:
                invalid.append({
                    "reason": "missing_entity_id",
                    "entry": entry,
                })

            if not path:
                invalid.append({
                    "reason": "missing_path",
                    "entry": entry,
                })

            if not identity_id:
                invalid.append({
                    "reason": "missing_identity_id",
                    "entry": entry,
                })

            if path:
                paths.setdefault(path, []).append(
                    entity_id
                )

        for path, entity_ids in paths.items():

            if len(entity_ids) > 1:
                invalid.append({
                    "reason": "duplicate_path",
                    "path": path,
                    "entity_ids": entity_ids,
                })

        return {
            "system": "registry",
            "total": len(entries),
            "invalid": len(invalid),
            "status": (
                "HEALTHY"
                if not invalid
                else "INCONSISTENT"
            ),
            "issues": invalid,
        }

    # ==========================================================
    # IDENTITY CHECK
    # ==========================================================

    def identity_check(self) -> dict:
        """
        Verify that every registered entity has a
        corresponding identity mapping.
        """

        entries = registry.list_all()
        identities = {
            item["entity_id"]
            for item in identity_manager.list_all()
        }

        missing = []

        for entry in entries:

            identity_id = entry.get(
                "identity_id"
            )

            if identity_id not in identities:
                missing.append({
                    "reason": "missing_identity",
                    "entity_id": entry.get(
                        "entity_id"
                    ),
                    "identity_id": identity_id,
                })

        return {
            "system": "identity",
            "registered_entities": len(entries),
            "identity_records": len(identities),
            "missing": len(missing),
            "status": (
                "HEALTHY"
                if not missing
                else "INCONSISTENT"
            ),
            "issues": missing,
        }

    # ==========================================================
    # DEPENDENCY CHECK
    # ==========================================================

    def dependency_check(self) -> dict:
        """
        Check dependencies for orphan entity references.
        """

        dependencies = dependency_index.list_all()

        orphaned = []

        for dependency in dependencies:

            source = registry.get(
                dependency["source_id"]
            )

            target = registry.get(
                dependency["target_id"]
            )

            if source is None:
                orphaned.append({
                    "type": "missing_source",
                    "dependency": dependency,
                })

            if target is None:
                orphaned.append({
                    "type": "missing_target",
                    "dependency": dependency,
                })

        return {
            "system": "dependencies",
            "total": len(dependencies),
            "orphaned": len(orphaned),
            "status": (
                "HEALTHY"
                if not orphaned
                else "INCONSISTENT"
            ),
            "issues": orphaned,
        }

    # ==========================================================
    # FILESYSTEM CHECK
    # ==========================================================

    def filesystem_check(
        self,
        root=None,
    ) -> dict:
        """
        Verify that registered filesystem paths exist.

        If root is not supplied, filesystem validation is
        limited to structural registry checks.
        """

        if root is None:
            return {
                "system": "filesystem",
                "status": "SKIPPED",
                "reason": "root_not_provided",
                "checked": 0,
                "missing": 0,
                "issues": [],
            }

        foundation_root = Path(
            root
        ).resolve()

        entries = registry.list_all()

        missing = []

        for entry in entries:

            relative_path = entry.get(
                "path"
            )

            if not relative_path:
                continue

            candidate = (
                foundation_root
                / relative_path
            ).resolve()

            try:
                candidate.relative_to(
                    foundation_root
                )
            except ValueError:

                missing.append({
                    "reason": "path_outside_root",
                    "entity_id": entry.get(
                        "entity_id"
                    ),
                    "path": relative_path,
                })

                continue

            if not candidate.exists():

                missing.append({
                    "reason": "missing_filesystem_path",
                    "entity_id": entry.get(
                        "entity_id"
                    ),
                    "path": relative_path,
                })

        return {
            "system": "filesystem",
            "status": (
                "HEALTHY"
                if not missing
                else "INCONSISTENT"
            ),
            "checked": len(entries),
            "missing": len(missing),
            "issues": missing,
        }

    # ==========================================================
    # COMPLETE CHECK
    # ==========================================================

    def check(
        self,
        root=None,
    ) -> dict:
        """
        Run the complete Foundation integrity suite.
        """

        registry_result = (
            self.registry_check()
        )

        identity_result = (
            self.identity_check()
        )

        dependency_result = (
            self.dependency_check()
        )

        filesystem_result = (
            self.filesystem_check(root)
        )

        filesystem_healthy = (
            filesystem_result["status"]
            in {
                "HEALTHY",
                "SKIPPED",
            }
        )

        healthy = (
            registry_result["status"]
            == "HEALTHY"
            and identity_result["status"]
            == "HEALTHY"
            and dependency_result["status"]
            == "HEALTHY"
            and filesystem_healthy
        )

        return {
            "status": (
                "HEALTHY"
                if healthy
                else "INCONSISTENT"
            ),
            "registry": registry_result,
            "identity": identity_result,
            "dependencies": dependency_result,
            "filesystem": filesystem_result,
        }


integrity = FoundationIntegrity()


__all__ = [
    "FoundationIntegrity",
    "integrity",
]
