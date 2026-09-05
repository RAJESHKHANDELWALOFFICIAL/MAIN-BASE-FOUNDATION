"""
MAIN BASE FOUNDATION
Central Synchronization Engine

Synchronizes the actual filesystem state with
the Central Foundation Registry.
"""

from pathlib import Path
from datetime import datetime, timezone

from foundation.registry.registry import (
    RegistryEntry,
    registry,
)


class SyncEngine:
    """
    Synchronizes filesystem entities with the
    central foundation registry.
    """

    def __init__(self, root: str):
        self.root = Path(root).resolve()

    def _resolve(self, path: str) -> Path:
        target = (self.root / path).resolve()

        if target != self.root and self.root not in target.parents:
            raise PermissionError(
                "Path is outside MAIN-BASE-FOUNDATION."
            )

        return target

    def _relative(self, path: Path) -> str:
        return str(
            path.relative_to(self.root)
        )

    def _entity_id(self, path: Path) -> str:
        """
        Generate a stable registry key from the
        current relative filesystem path.

        Existing registered entities should retain
        their original entity_id when possible.
        """

        return self._relative(path).replace(
            "\\",
            "/"
        )

    def scan_filesystem(self) -> list[dict]:
        """
        Scan the complete foundation filesystem.
        """

        results = []

        for item in self.root.rglob("*"):

            if not item.exists():
                continue

            results.append(
                {
                    "path": self._relative(item),
                    "type": (
                        "directory"
                        if item.is_dir()
                        else "file"
                    ),
                }
            )

        return sorted(
            results,
            key=lambda item: item["path"].lower()
        )

    def synchronize(self) -> dict:
        """
        Synchronize filesystem state with registry.

        Returns a summary of changes.
        """

        filesystem_items = {
            item["path"]: item
            for item in self.scan_filesystem()
        }

        registered_items = {
            entry.path: entry
            for entry in registry._entries.values()
        }

        created = []
        removed = []
        updated = []

        # Register filesystem items that are not
        # currently present in the registry.
        for path, item in filesystem_items.items():

            if path not in registered_items:

                entity_id = self._entity_id(
                    self.root / path
                )

                identity_id = entity_id

                registry.register(
                    RegistryEntry(
                        entity_id=entity_id,
                        entity_type=item["type"],
                        path=path,
                        identity_id=identity_id,
                    )
                )

                created.append(path)

        # Remove registry entries whose filesystem
        # objects no longer exist.
        for path, entry in registered_items.items():

            target = self._resolve(path)

            if not target.exists():

                registry.remove(
                    entry.entity_id
                )

                removed.append(path)

        # Ensure registry paths and filesystem types
        # remain consistent.
        for path, item in filesystem_items.items():

            entry = registry._entries.get(
                self._entity_id(
                    self.root / path
                )
            )

            if entry is None:
                continue

            changed = False

            if entry.path != path:
                entry.path = path
                changed = True

            if entry.entity_type != item["type"]:
                entry.entity_type = item["type"]
                changed = True

            if changed:

                entry.updated_at = (
                    datetime.now(
                        timezone.utc
                    ).isoformat()
                )

                updated.append(path)

        return {
            "success": True,
            "created": created,
            "removed": removed,
            "updated": updated,
            "total_filesystem_items": len(
                filesystem_items
            ),
            "total_registry_items": len(
                registry._entries
            ),
        }


__all__ = [
    "SyncEngine",
]
