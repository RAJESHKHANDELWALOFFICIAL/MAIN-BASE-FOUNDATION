"""
MAIN BASE FOUNDATION
Filesystem Synchronization Engine

Synchronizes the real filesystem with the Foundation Registry
while preserving stable entity identities.
"""

from pathlib import Path

from foundation.registry.registry import registry


class SyncEngine:

    def __init__(self, root: str):
        self.root = Path(root).resolve()

    def _resolve(self, path: str) -> Path:
        candidate = Path(path)

        if not candidate.is_absolute():
            candidate = self.root / candidate

        resolved = candidate.resolve()

        try:
            resolved.relative_to(self.root)
        except ValueError:
            raise ValueError(
                f"Path is outside foundation root: {path}"
            )

        return resolved

    def _relative(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def scan_filesystem(self) -> dict[str, str]:
        """
        Return filesystem items indexed by relative path.
        """

        items = {}

        for path in self.root.rglob("*"):

            if not path.exists():
                continue

            if ".git" in path.parts:
                continue

            relative = self._relative(path)

            if path.is_dir():
                items[relative] = "folder"
            elif path.is_file():
                items[relative] = "file"

        return items

    def synchronize(self) -> dict:
        """
        Synchronize filesystem state with the registry.

        Existing registry entries retain their entity IDs.
        Filesystem paths are treated as the current location
        of those entities.
        """

        filesystem = self.scan_filesystem()

        entries = registry.list_all()

        registry_by_path = {
            entry["path"]: entry
            for entry in entries
            if entry.get("path")
        }

        registered_paths = set(registry_by_path.keys())
        filesystem_paths = set(filesystem.keys())

        registered = 0
        updated = 0
        removed = 0

        # --------------------------------------------------
        # REGISTER NEW FILESYSTEM ITEMS
        # --------------------------------------------------

        for path in sorted(
            filesystem_paths - registered_paths
        ):
            entity_type = filesystem[path]

            entity_id = (
                f"filesystem:{path}"
            )

            registry.register(
                entity_id=entity_id,
                entity_type=entity_type,
                path=path,
                identity_id=entity_id,
            )

            registered += 1

        # --------------------------------------------------
        # UPDATE EXISTING ITEMS
        # --------------------------------------------------

        for path in sorted(
            filesystem_paths & registered_paths
        ):
            entry = registry_by_path[path]

            if entry.get("status") != "active":
                registry.update(
                    entry["entity_id"],
                    status="active",
                )

                updated += 1

        # --------------------------------------------------
        # REMOVE MISSING ITEMS
        # --------------------------------------------------

        for path in sorted(
            registered_paths - filesystem_paths
        ):
            entry = registry_by_path[path]

            try:
                registry.remove(
                    entry["entity_id"]
                )
                removed += 1

            except KeyError:
                pass

        return {
            "root": str(self.root),
            "filesystem_items": len(filesystem),
            "registered": registered,
            "updated": updated,
            "removed": removed,
            "status": "SYNCHRONIZED",
        }


__all__ = [
    "SyncEngine",
]
