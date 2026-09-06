"""
MAIN BASE FOUNDATION
Central Synchronization Engine

Synchronizes the actual filesystem state with
the persistent Foundation Registry.
"""

from datetime import datetime, timezone
from pathlib import Path

from foundation.registry.registry import (
    RegistryEntry,
    registry,
)


class SyncEngine:
    """
    Synchronizes filesystem state with the Foundation Registry.

    The filesystem is the source of truth for physical existence.
    Registry entity IDs remain stable whenever an existing registered
    entity can be matched to its current filesystem path.
    """

    def __init__(self, root: str):
        self.root = Path(root).resolve()

    def _resolve(self, path: str) -> Path:
        """Resolve a path while enforcing the foundation root."""

        target = (self.root / path).resolve()

        if (
            target != self.root
            and self.root not in target.parents
        ):
            raise PermissionError(
                "Path is outside MAIN-BASE-FOUNDATION."
            )

        return target

    def _relative(self, path: Path) -> str:
        """Return a normalized path relative to foundation root."""

        return str(
            path.relative_to(self.root)
        ).replace("\\", "/")

    def scan_filesystem(self) -> list[dict]:
        """Scan all filesystem items below the foundation root."""

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
            key=lambda item: item["path"].lower(),
        )

    def _registry_entries(self) -> list[RegistryEntry]:
        """Return all persistent registry entries."""

        entries = []

        for item in registry.list_all():
            entries.append(
                RegistryEntry(
                    entity_id=item["entity_id"],
                    entity_type=item["entity_type"],
                    path=item["path"],
                    identity_id=item["identity_id"],
                    status=item["status"],
                    created_at=item["created_at"],
                    updated_at=item["updated_at"],
                )
            )

        return entries

    def _create_registry_entry(
        self,
        path: str,
        entity_type: str,
    ) -> RegistryEntry:
        """Create a new registry entry for an unregistered item."""

        entity_id = path
        identity_id = path

        existing = registry.get(entity_id)

        if existing is not None:
            entity_id = f"{entity_type}:{path}"
            identity_id = entity_id

        entry = RegistryEntry(
            entity_id=entity_id,
            entity_type=entity_type,
            path=path,
            identity_id=identity_id,
        )

        registry.register(entry)

        return entry

    def synchronize(self) -> dict:
        """
        Synchronize filesystem and persistent registry.

        New filesystem items are registered.

        Missing filesystem items are removed from the registry.

        Existing registered items retain their entity IDs while
        their metadata is synchronized.
        """

        filesystem_items = self.scan_filesystem()

        filesystem_by_path = {
            item["path"]: item
            for item in filesystem_items
        }

        registered_entries = self._registry_entries()

        registered_by_path = {
            entry.path: entry
            for entry in registered_entries
        }

        created = []
        removed = []
        updated = []
        unchanged = []

        # ---------------------------------------------------------
        # 1. REGISTER NEW FILESYSTEM ITEMS
        # ---------------------------------------------------------

        for path, item in filesystem_by_path.items():

            if path not in registered_by_path:

                entry = self._create_registry_entry(
                    path=path,
                    entity_type=item["type"],
                )

                created.append(
                    {
                        "entity_id": entry.entity_id,
                        "path": entry.path,
                        "type": entry.entity_type,
                    }
                )

        # ---------------------------------------------------------
        # 2. REMOVE REGISTRY ITEMS THAT NO LONGER EXIST
        # ---------------------------------------------------------

        for entry in registered_entries:

            target = self._resolve(entry.path)

            if not target.exists():

                try:
                    registry.remove(
                        entry.entity_id
                    )

                    removed.append(
                        {
                            "entity_id": entry.entity_id,
                            "path": entry.path,
                        }
                    )

                except KeyError:
                    pass

        # ---------------------------------------------------------
        # 3. UPDATE EXISTING REGISTRY METADATA
        # ---------------------------------------------------------

        for path, item in filesystem_by_path.items():

            entry = registry.find_by_path(path)

            if entry is None:
                continue

            changes = {}

            if entry.entity_type != item["type"]:
                changes["entity_type"] = item["type"]

            if entry.status != "active":
                changes["status"] = "active"

            if changes:
                registry.update(
                    entry.entity_id,
                    **changes,
                )

                updated.append(
                    {
                        "entity_id": entry.entity_id,
                        "path": path,
                        "changes": changes,
                    }
                )

            else:
                unchanged.append(
                    {
                        "entity_id": entry.entity_id,
                        "path": path,
                    }
                )

        return {
            "success": True,
            "created": created,
            "removed": removed,
            "updated": updated,
            "unchanged": unchanged,
            "total_filesystem_items": len(
                filesystem_items
            ),
            "total_registry_items": registry.count(),
        }

    def status(self) -> dict:
        """Return synchronization status."""

        filesystem_count = len(
            self.scan_filesystem()
        )

        registry_count = registry.count()

        return {
            "engine": "FOUNDATION SYNCHRONIZATION",
            "status": "READY",
            "root": str(self.root),
            "filesystem_items": filesystem_count,
            "registry_items": registry_count,
            "in_sync": (
                filesystem_count
                == registry_count
            ),
        }


__all__ = [
    "SyncEngine",
]
