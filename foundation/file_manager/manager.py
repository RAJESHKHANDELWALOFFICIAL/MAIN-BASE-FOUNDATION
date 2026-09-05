"""
MAIN BASE FOUNDATION
Central File Manager

Central filesystem operations with security,
registry and audit integration.
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
    MAIN-BASE-FOUNDATION.
    """

    def __init__(self, root: str):
        self.root = Path(root).resolve()

    def _resolve(self, path: str) -> Path:
        target = (self.root / path).resolve()

        if (
            target != self.root
            and self.root not in target.parents
        ):
            raise PermissionError(
                "Path is outside MAIN-BASE-FOUNDATION."
            )

        return target

    def _authorize(
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

    def _audit(
        self,
        operation: str,
        entity_id: str,
        path: str,
        subject_id: str,
        status: str,
        details: str = "",
    ) -> None:

        audit_log.record(
            operation=operation,
            entity_id=entity_id,
            path=path,
            subject_id=subject_id,
            status=status,
            details=details,
        )

    def create_folder(
        self,
        path: str,
        entity_id: str,
        identity_id: str,
        subject_id: str,
    ) -> str:

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

            relative_path = str(
                target.relative_to(self.root)
            )

            registry.register(
                RegistryEntry(
                    entity_id=entity_id,
                    entity_type="directory",
                    path=relative_path,
                    identity_id=identity_id,
                )
            )

            self._audit(
                operation="create",
                entity_id=entity_id,
                path=relative_path,
                subject_id=subject_id,
                status="success",
                details="Directory created.",
            )

            return relative_path

        except Exception as error:

            self._audit(
                operation="create",
                entity_id=entity_id,
                path=path,
                subject_id=subject_id,
                status="failed",
                details=str(error),
            )

            raise

    def create_file(
        self,
        path: str,
        entity_id: str,
        identity_id: str,
        subject_id: str,
        content: str = "",
    ) -> str:

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

            relative_path = str(
                target.relative_to(self.root)
            )

            registry.register(
                RegistryEntry(
                    entity_id=entity_id,
                    entity_type="file",
                    path=relative_path,
                    identity_id=identity_id,
                )
            )

            self._audit(
                operation="create",
                entity_id=entity_id,
                path=relative_path,
                subject_id=subject_id,
                status="success",
                details="File created.",
            )

            return relative_path

        except Exception as error:

            self._audit(
                operation="create",
                entity_id=entity_id,
                path=path,
                subject_id=subject_id,
                status="failed",
                details=str(error),
            )

            raise

    def rename(
        self,
        entity_id: str,
        destination: str,
        subject_id: str,
    ) -> str:

        entry = registry.get(entity_id)
        old_path = entry.path

        self._authorize(
            subject_id,
            "rename",
            old_path,
        )

        source_path = self._resolve(
            old_path
        )

        destination_path = self._resolve(
            destination
        )

        if not source_path.exists():
            raise FileNotFoundError(
                f"Source does not exist: {old_path}"
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

            source_path.rename(
                destination_path
            )

            relative_path = str(
                destination_path.relative_to(self.root)
            )

            registry.update_path(
                entity_id,
                relative_path,
            )

            self._audit(
                operation="rename",
                entity_id=entity_id,
                path=relative_path,
                subject_id=subject_id,
                status="success",
                details=(
                    f"Renamed from {old_path}."
                ),
            )

            return relative_path

        except Exception as error:

            self._audit(
                operation="rename",
                entity_id=entity_id,
                path=destination,
                subject_id=subject_id,
                status="failed",
                details=str(error),
            )

            raise

    def move(
        self,
        entity_id: str,
        destination: str,
        subject_id: str,
    ) -> str:

        entry = registry.get(entity_id)
        old_path = entry.path

        self._authorize(
            subject_id,
            "move",
            old_path,
        )

        source_path = self._resolve(
            old_path
        )

        destination_path = self._resolve(
            destination
        )

        if not source_path.exists():
            raise FileNotFoundError(
                f"Source does not exist: {old_path}"
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

            shutil.move(
                str(source_path),
                str(destination_path),
            )

            relative_path = str(
                destination_path.relative_to(self.root)
            )

            registry.update_path(
                entity_id,
                relative_path,
            )

            self._audit(
                operation="move",
                entity_id=entity_id,
                path=relative_path,
                subject_id=subject_id,
                status="success",
                details=(
                    f"Moved from {old_path}."
                ),
            )

            return relative_path

        except Exception as error:

            self._audit(
                operation="move",
                entity_id=entity_id,
                path=destination,
                subject_id=subject_id,
                status="failed",
                details=str(error),
            )

            raise

    def copy(
        self,
        source_entity_id: str,
        destination: str,
        entity_id: str,
        identity_id: str,
        subject_id: str,
    ) -> str:

        source_entry = registry.get(
            source_entity_id
        )

        self._authorize(
            subject_id,
            "copy",
            source_entry.path,
        )

        source_path = self._resolve(
            source_entry.path
        )

        destination_path = self._resolve(
            destination
        )

        if not source_path.exists():
            raise FileNotFoundError(
                f"Source does not exist: "
                f"{source_entry.path}"
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

            relative_path = str(
                destination_path.relative_to(
                    self.root
                )
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
                operation="copy",
                entity_id=entity_id,
                path=relative_path,
                subject_id=subject_id,
                status="success",
                details=(
                    f"Copied from "
                    f"{source_entry.path}."
                ),
            )

            return relative_path

        except Exception as error:

            self._audit(
                operation="copy",
                entity_id=entity_id,
                path=destination,
                subject_id=subject_id,
                status="failed",
                details=str(error),
            )

            raise

    def delete(
        self,
        entity_id: str,
        subject_id: str,
    ) -> bool:

        entry = registry.get(entity_id)

        self._authorize(
            subject_id,
            "delete",
            entry.path,
        )

        target = self._resolve(
            entry.path
        )

        if target == self.root:
            raise PermissionError(
                "MAIN-BASE-FOUNDATION root "
                "cannot be deleted."
            )

        if not target.exists():
            raise FileNotFoundError(
                f"Item does not exist: "
                f"{entry.path}"
            )

        try:
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()

            registry.remove(
                entity_id
            )

            self._audit(
                operation="delete",
                entity_id=entity_id,
                path=entry.path,
                subject_id=subject_id,
                status="success",
                details="Entity deleted.",
            )

            return True

        except Exception as error:

            self._audit(
                operation="delete",
                entity_id=entity_id,
                path=entry.path,
                subject_id=subject_id,
                status="failed",
                details=str(error),
            )

            raise

    def list_directory(
        self,
        path: str = ".",
        subject_id: str = "",
    ) -> list[dict]:

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

        return [
            {
                "name": item.name,
                "path": str(
                    item.relative_to(self.root)
                ),
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


__all__ = [
    "FileManager",
]
