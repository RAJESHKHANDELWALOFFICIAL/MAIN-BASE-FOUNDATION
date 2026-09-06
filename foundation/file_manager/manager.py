"""
MAIN BASE FOUNDATION
Central File Manager

Central filesystem operations with security,
persistent registry and audit integration.
"""

from pathlib import Path
import shutil

from foundation.audit.audit import audit_log
from foundation.registry.registry import (
    RegistryEntry,
    registry,
)
from foundation.security.access import (
    access_controller,
)


class FileManager:
    """
    Central filesystem manager for the entire
    MAIN-BASE-FOUNDATION system.
    """

    def __init__(self, root: str):
        self.root = Path(root).resolve()

    # ==========================================================
    # INTERNAL PATH MANAGEMENT
    # ==========================================================

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
        """Return normalized path relative to foundation root."""

        return str(
            path.relative_to(self.root)
        ).replace("\\", "/")

    def _authorize(
        self,
        subject_id: str,
        operation: str,
        path: str,
    ) -> None:
        """Authorize an operation against a path."""

        access_controller.authorize_path(
            subject_id=subject_id,
            operation=operation,
            path=path,
        )

    def _audit(
        self,
        operation: str,
        entity_id: str,
        path: str,
        subject_id: str,
        status: str,
        details: str = "",
    ) -> None:
        """Write an operation to persistent audit history."""

        audit_log.record(
            operation=operation,
            entity_id=entity_id,
            path=path,
            subject_id=subject_id,
            status=status,
            details=details,
        )

    # ==========================================================
    # CREATE
    # ==========================================================

    def create_folder(
        self,
        path,
        entity_id,
        identity_id,
        subject_id,
    ) -> str:
        """Create and register a directory."""

        self._authorize(
            subject_id,
            "create",
            path,
        )

        target = self._resolve(path)

        if target.exists():
            raise FileExistsError(
                f"Item already exists: {path}"
            )

        try:
            target.mkdir(
                parents=True,
                exist_ok=False,
            )

            relative_path = self._relative(target)

            registry.register(
                RegistryEntry(
                    entity_id=entity_id,
                    entity_type="directory",
                    path=relative_path,
                    identity_id=identity_id,
                )
            )

            self._audit(
                "create",
                entity_id,
                relative_path,
                subject_id,
                "success",
                "Directory created.",
            )

            return relative_path

        except Exception as error:
            if target.exists():
                try:
                    target.rmdir()
                except OSError:
                    pass

            self._audit(
                "create",
                entity_id,
                path,
                subject_id,
                "failed",
                str(error),
            )

            raise

    def create_file(
        self,
        path,
        entity_id,
        identity_id,
        subject_id,
        content="",
    ) -> str:
        """Create and register a file."""

        self._authorize(
            subject_id,
            "create",
            path,
        )

        target = self._resolve(path)

        if target.exists():
            raise FileExistsError(
                f"Item already exists: {path}"
            )

        try:
            target.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            target.write_text(
                content,
                encoding="utf-8",
            )

            relative_path = self._relative(target)

            registry.register(
                RegistryEntry(
                    entity_id=entity_id,
                    entity_type="file",
                    path=relative_path,
                    identity_id=identity_id,
                )
            )

            self._audit(
                "create",
                entity_id,
                relative_path,
                subject_id,
                "success",
                "File created.",
            )

            return relative_path

        except Exception as error:
            if target.exists():
                try:
                    target.unlink()
                except OSError:
                    pass

            self._audit(
                "create",
                entity_id,
                path,
                subject_id,
                "failed",
                str(error),
            )

            raise

    # ==========================================================
    # READ
    # ==========================================================

    def read_file(
        self,
        path: str,
        subject_id: str,
    ) -> str:
        """Read a file through the central file manager."""

        self._authorize(
            subject_id,
            "read",
            path,
        )

        target = self._resolve(path)

        if not target.exists():
            raise FileNotFoundError(
                f"File does not exist: {path}"
            )

        if not target.is_file():
            raise IsADirectoryError(
                f"Not a file: {path}"
            )

        try:
            content = target.read_text(
                encoding="utf-8"
            )

            self._audit(
                "read",
                "",
                path,
                subject_id,
                "success",
                "File read.",
            )

            return content

        except Exception as error:
            self._audit(
                "read",
                "",
                path,
                subject_id,
                "failed",
                str(error),
            )

            raise

    # ==========================================================
    # SEARCH
    # ==========================================================

    def search(
        self,
        query: str,
        subject_id: str,
        path: str = ".",
    ) -> list[dict]:
        """
        Search filenames and directory names recursively.

        Search is intentionally filesystem-based. The Registry
        remains the metadata source while the filesystem remains
        the physical source of truth.
        """

        if not query:
            raise ValueError(
                "Search query cannot be empty."
            )

        self._authorize(
            subject_id,
            "search",
            path,
        )

        target = self._resolve(path)

        if not target.exists():
            raise FileNotFoundError(
                f"Search path does not exist: {path}"
            )

        if not target.is_dir():
            raise NotADirectoryError(
                f"Search path is not a directory: {path}"
            )

        query_lower = query.lower()
        results = []

        for item in target.rglob("*"):
            if query_lower in item.name.lower():
                results.append(
                    {
                        "name": item.name,
                        "path": self._relative(item),
                        "type": (
                            "directory"
                            if item.is_dir()
                            else "file"
                        ),
                    }
                )

        results.sort(
            key=lambda item: item["path"].lower()
        )

        self._audit(
            "search",
            "",
            path,
            subject_id,
            "success",
            f"Search query: {query}",
        )

        return results

    # ==========================================================
    # RENAME
    # ==========================================================

    def rename(
        self,
        entity_id,
        destination,
        subject_id,
    ) -> str:
        """Rename an existing registered entity."""

        entry = registry.require(entity_id)

        old_path = entry.path

        self._authorize(
            subject_id,
            "rename",
            old_path,
        )

        self._authorize(
            subject_id,
            "rename",
            destination,
        )

        source_path = self._resolve(old_path)
        destination_path = self._resolve(destination)

        if not source_path.exists():
            raise FileNotFoundError(
                f"Source does not exist: {old_path}"
            )

        if destination_path.exists():
            raise FileExistsError(
                f"Destination already exists: {destination}"
            )

        try:
            destination_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            source_path.rename(
                destination_path
            )

            relative_path = self._relative(
                destination_path
            )

            registry.update_path(
                entity_id,
                relative_path,
            )

            self._audit(
                "rename",
                entity_id,
                relative_path,
                subject_id,
                "success",
                f"Renamed from {old_path}.",
            )

            return relative_path

        except Exception as error:
            self._audit(
                "rename",
                entity_id,
                destination,
                subject_id,
                "failed",
                str(error),
            )

            raise

    # ==========================================================
    # MOVE
    # ==========================================================

    def move(
        self,
        entity_id,
        destination,
        subject_id,
    ) -> str:
        """Move an existing registered entity."""

        entry = registry.require(entity_id)

        old_path = entry.path

        self._authorize(
            subject_id,
            "move",
            old_path,
        )

        self._authorize(
            subject_id,
            "move",
            destination,
        )

        source_path = self._resolve(old_path)
        destination_path = self._resolve(destination)

        if not source_path.exists():
            raise FileNotFoundError(
                f"Source does not exist: {old_path}"
            )

        if destination_path.exists():
            raise FileExistsError(
                f"Destination already exists: {destination}"
            )

        try:
            destination_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.move(
                str(source_path),
                str(destination_path),
            )

            relative_path = self._relative(
                destination_path
            )

            registry.update_path(
                entity_id,
                relative_path,
            )

            self._audit(
                "move",
                entity_id,
                relative_path,
                subject_id,
                "success",
                f"Moved from {old_path}.",
            )

            return relative_path

        except Exception as error:
            self._audit(
                "move",
                entity_id,
                destination,
                subject_id,
                "failed",
                str(error),
            )

            raise

    # ==========================================================
    # COPY
    # ==========================================================

    def copy(
        self,
        source_entity_id,
        destination,
        entity_id,
        identity_id,
        subject_id,
    ) -> str:
        """Copy an entity and register the new entity."""

        source_entry = registry.require(
            source_entity_id
        )

        source_path_value = source_entry.path

        self._authorize(
            subject_id,
            "copy",
            source_path_value,
        )

        self._authorize(
            subject_id,
            "copy",
            destination,
        )

        source_path = self._resolve(
            source_path_value
        )

        destination_path = self._resolve(
            destination
        )

        if not source_path.exists():
            raise FileNotFoundError(
                f"Source does not exist: "
                f"{source_path_value}"
            )

        if destination_path.exists():
            raise FileExistsError(
                f"Destination already exists: "
                f"{destination}"
            )

        try:
            destination_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            if source_path.is_dir():
                shutil.copytree(
                    source_path,
                    destination_path,
                )
                entity_type = "directory"

            else:
                shutil.copy2(
                    source_path,
                    destination_path,
                )
                entity_type = "file"

            relative_path = self._relative(
                destination_path
            )

            registry.register(
                RegistryEntry(
                    entity_id=entity_id,
                    entity_type=entity_type,
                    path=relative_path,
                    identity_id=identity_id,
                )
            )

            self._audit(
                "copy",
                entity_id,
                relative_path,
                subject_id,
                "success",
                f"Copied from {source_path_value}.",
            )

            return relative_path

        except Exception as error:
            if destination_path.exists():
                try:
                    if destination_path.is_dir():
                        shutil.rmtree(
                            destination_path
                        )
                    else:
                        destination_path.unlink()
                except OSError:
                    pass

            self._audit(
                "copy",
                entity_id,
                destination,
                subject_id,
                "failed",
                str(error),
            )

            raise

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete(
        self,
        entity_id,
        subject_id,
    ) -> bool:
        """Delete an entity and its registry descendants."""

        entry = registry.require(entity_id)

        original_path = entry.path

        self._authorize(
            subject_id,
            "delete",
            original_path,
        )

        target = self._resolve(
            original_path
        )

        if target == self.root:
            raise PermissionError(
                "MAIN-BASE-FOUNDATION root "
                "cannot be deleted."
            )

        if not target.exists():
            raise FileNotFoundError(
                f"Item does not exist: "
                f"{original_path}"
            )

        try:
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()

            # Remove the primary registry entity.
            registry.remove(entity_id)

            # Remove registered descendants when a directory
            # is deleted.
            prefix = (
                original_path.rstrip("/")
                + "/"
            )

            for item in registry.list_all():
                item_path = item["path"]

                if item_path.startswith(prefix):
                    try:
                        registry.remove(
                            item["entity_id"]
                        )
                    except KeyError:
                        pass

            self._audit(
                "delete",
                entity_id,
                original_path,
                subject_id,
                "success",
                "Entity deleted.",
            )

            return True

        except Exception as error:
            self._audit(
                "delete",
                entity_id,
                original_path,
                subject_id,
                "failed",
                str(error),
            )

            raise

    # ==========================================================
    # LIST
    # ==========================================================

    def list_directory(
        self,
        path=".",
        subject_id="",
    ) -> list[dict]:
        """List directory contents."""

        self._authorize(
            subject_id,
            "list",
            path,
        )

        target = self._resolve(path)

        if not target.exists():
            raise FileNotFoundError(
                f"Directory does not exist: {path}"
            )

        if not target.is_dir():
            raise NotADirectoryError(
                f"Not a directory: {path}"
            )

        results = [
            {
                "name": item.name,
                "path": self._relative(item),
                "type": (
                    "directory"
                    if item.is_dir()
                    else "file"
                ),
            }
            for item in sorted(
                target.iterdir(),
                key=lambda item: item.name.lower(),
            )
        ]

        self._audit(
            "list",
            "",
            path,
            subject_id,
            "success",
            "Directory listed.",
        )

        return results


__all__ = [
    "FileManager",
]
