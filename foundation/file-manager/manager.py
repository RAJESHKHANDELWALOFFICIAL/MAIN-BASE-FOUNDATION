"""
MAIN BASE FOUNDATION
Central File and Folder Manager

Manages files and folders across the entire
MAIN-BASE-FOUNDATION.
"""

from pathlib import Path
import shutil


class FileManager:
    """
    Central filesystem manager.
    """

    def __init__(self, root: str):
        self.root = Path(root).resolve()

    def _resolve(self, path: str) -> Path:
        """
        Resolve a path and keep it inside
        MAIN-BASE-FOUNDATION.
        """

        target = (self.root / path).resolve()

        if target != self.root and self.root not in target.parents:
            raise PermissionError(
                "Path is outside MAIN-BASE-FOUNDATION."
            )

        return target

    def exists(self, path: str) -> bool:
        return self._resolve(path).exists()

    def create_folder(self, path: str) -> str:
        target = self._resolve(path)

        if target.exists():
            raise FileExistsError(
                f"Item already exists: {path}"
            )

        target.mkdir(
            parents=True,
            exist_ok=False
        )

        return str(target.relative_to(self.root))

    def create_file(
        self,
        path: str,
        content: str = ""
    ) -> str:

        target = self._resolve(path)

        if target.exists():
            raise FileExistsError(
                f"Item already exists: {path}"
            )

        target.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        target.write_text(
            content,
            encoding="utf-8"
        )

        return str(target.relative_to(self.root))

    def rename(
        self,
        source: str,
        destination: str
    ) -> str:

        source_path = self._resolve(source)
        destination_path = self._resolve(destination)

        if not source_path.exists():
            raise FileNotFoundError(
                f"Source does not exist: {source}"
            )

        if destination_path.exists():
            raise FileExistsError(
                f"Destination already exists: {destination}"
            )

        destination_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        source_path.rename(destination_path)

        return str(
            destination_path.relative_to(self.root)
        )

    def move(
        self,
        source: str,
        destination: str
    ) -> str:

        source_path = self._resolve(source)
        destination_path = self._resolve(destination)

        if not source_path.exists():
            raise FileNotFoundError(
                f"Source does not exist: {source}"
            )

        if destination_path.exists():
            raise FileExistsError(
                f"Destination already exists: {destination}"
            )

        destination_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.move(
            str(source_path),
            str(destination_path)
        )

        return str(
            destination_path.relative_to(self.root)
        )

    def copy(
        self,
        source: str,
        destination: str
    ) -> str:

        source_path = self._resolve(source)
        destination_path = self._resolve(destination)

        if not source_path.exists():
            raise FileNotFoundError(
                f"Source does not exist: {source}"
            )

        if destination_path.exists():
            raise FileExistsError(
                f"Destination already exists: {destination}"
            )

        destination_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if source_path.is_dir():
            shutil.copytree(
                source_path,
                destination_path
            )
        else:
            shutil.copy2(
                source_path,
                destination_path
            )

        return str(
            destination_path.relative_to(self.root)
        )

    def delete(self, path: str) -> bool:

        target = self._resolve(path)

        if not target.exists():
            raise FileNotFoundError(
                f"Item does not exist: {path}"
            )

        if target == self.root:
            raise PermissionError(
                "MAIN-BASE-FOUNDATION root cannot be deleted."
            )

        if target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()

        return True

    def list_directory(
        self,
        path: str = "."
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
                key=lambda item: item.name.lower()
            )
        ]


__all__ = [
    "FileManager",
]
