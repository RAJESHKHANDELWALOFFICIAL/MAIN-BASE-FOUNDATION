"""
MAIN BASE FOUNDATION
Foundation Integrity Layer

Central consistency checks for Registry, Dependencies,
Filesystem and Audit systems.
"""

from foundation.dependencies.index import dependency_index
from foundation.registry.registry import registry


class FoundationIntegrity:

    def registry_check(self) -> dict:
        """
        Check registry entries for basic structural validity.
        """

        entries = registry.list_all()

        invalid = []

        for entry in entries:

            if not entry.get("entity_id"):
                invalid.append(
                    {
                        "reason": "missing_entity_id",
                        "entry": entry,
                    }
                )

            if not entry.get("path"):
                invalid.append(
                    {
                        "reason": "missing_path",
                        "entry": entry,
                    }
                )

            if not entry.get("identity_id"):
                invalid.append(
                    {
                        "reason": "missing_identity_id",
                        "entry": entry,
                    }
                )

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
                orphaned.append(
                    {
                        "type": "missing_source",
                        "dependency": dependency,
                    }
                )

            if target is None:
                orphaned.append(
                    {
                        "type": "missing_target",
                        "dependency": dependency,
                    }
                )

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

    def check(self) -> dict:
        """
        Run all foundation integrity checks.
        """

        registry_result = (
            self.registry_check()
        )

        dependency_result = (
            self.dependency_check()
        )

        healthy = (
            registry_result["status"]
            == "HEALTHY"
            and dependency_result["status"]
            == "HEALTHY"
        )

        return {
            "status": (
                "HEALTHY"
                if healthy
                else "INCONSISTENT"
            ),
            "registry": registry_result,
            "dependencies": dependency_result,
        }


integrity = FoundationIntegrity()


__all__ = [
    "FoundationIntegrity",
    "integrity",
]
