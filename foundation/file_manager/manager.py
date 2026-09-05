"""
MAIN BASE FOUNDATION
Central File Manager

Filesystem operations connected to the
Central Foundation Registry.
"""

from pathlib import Path
import shutil

from foundation.registry.registry import (
    RegistryEntry,
    registry,
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

        if target != self.root and self.root not in target.parents:
            raise PermissionError(
                "Path is outside MAIN-BASE-FOUNDATION."
            )

        return target

    def create_folder(
        self,
        path: str,
        entity_id: str,
        identity_id: str,
    ) -> str:

        target = self._resolve(path)

        if target.exists():
            raise FileExistsError(
                f"Item already exists: {path}"
            )

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

        return relative_path

    def create_file(
        self,
        path: str,
        entity_id: str,
        identity_id: str,
        content: str = "",
    ) -> str:

        target = self._resolve(path)

        if target.exists():
            raise FileExistsError(
                f"Item already exists: {path}"
            )

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

        return relative_path

    def rename(
        self,
        entity_id: str,
        destination: str,
    ) -> str:

        entry = registry.get(entity_id)

        source_path = self._resolve(
            entry.path
        )

        destination_path = self._resolve(
            destination
        )

        if not source_path.exists():
            raise FileNotFoundError(
                f"Source does not exist: {entry.path}"
            )

        if destination_path.exists():
            raise FileExistsError(
                f"Destination already exists: {destination}"
            )

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

        return relative_path

    def move(
        self,
        entity_id: str,
        destination: str,
    ) -> str:

        entry = registry.get(entity_id)

        source_path = self._resolve(
            entry.path
        )

        destination_path = self._resolve(
            destination
        )

        if not source_path.exists():
            raise FileNotFoundError(
                f"Source does not exist: {entry.path}"
            )

        if destination_path.exists():
            raise FileExistsError(
                f"Destination already exists: {destination}"
            )

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

        return relative_path

    def copy(
        self,
        source_entity_id: str,
        destination: str,
        entity_id: str,
        identity_id: str,
    ) -> str:

        source_entry = registry.get(
            source_entity_id
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
            destination_path.relative_to(self.root)
        )

        registry.register(
            RegistryEntry(
                entity_id=entity_id,
                entity_type=entity_type,
                path=relative_path,
                identity_id=identity_id,
            )
        )

        return relative_path

    def delete(
        self,
        entity_id: str,
    ) -> bool:

        entry = registry.get(entity_id)

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
                f"Item does not exist: {entry.path}"
            )

        if target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()

        registry.remove(
            entity_id
        )

        return True

    def list_directory(
        self,
        path: str = ".",
    ) -> list[dict]:

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
