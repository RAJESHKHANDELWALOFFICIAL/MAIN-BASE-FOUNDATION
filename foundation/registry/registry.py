"""
MAIN BASE FOUNDATION
Central Persistent Foundation Registry

Maintains the canonical persistent registry of entities
belonging to MAIN-BASE-FOUNDATION.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from backend.engines.database.manager import DatabaseEngine


@dataclass
class RegistryEntry:
    entity_id: str
    entity_type: str
    path: str
    identity_id: str
    status: str = "active"
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        now = datetime.now(timezone.utc).isoformat()

        if not self.created_at:
            self.created_at = now

        if not self.updated_at:
            self.updated_at = now

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "path": self.path,
            "identity_id": self.identity_id,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class FoundationRegistry:
    """
    Persistent registry for MAIN-BASE-FOUNDATION.

    Filesystem remains the source of truth for physical files
    and directories. The registry stores their stable metadata.
    """

    TABLE_NAME = "foundation_registry"

    def __init__(
        self,
        database: Optional[DatabaseEngine] = None,
    ):
        self.database = database or DatabaseEngine()
        self._initialize()

    def _initialize(self) -> None:
        """Create the registry table when required."""

        self.database.create_table(
            f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                entity_id TEXT PRIMARY KEY,
                entity_type TEXT NOT NULL,
                path TEXT NOT NULL,
                identity_id TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'active',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        self.database.execute(
            f"""
            CREATE INDEX IF NOT EXISTS
            idx_{self.TABLE_NAME}_path
            ON {self.TABLE_NAME}(path)
            """
        )

    def register(self, entry: RegistryEntry) -> RegistryEntry:
        """Register a new entity."""

        existing = self.get(entry.entity_id)

        if existing is not None:
            raise ValueError(
                f"Entity already registered: {entry.entity_id}"
            )

        self.database.execute(
            f"""
            INSERT INTO {self.TABLE_NAME} (
                entity_id,
                entity_type,
                path,
                identity_id,
                status,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry.entity_id,
                entry.entity_type,
                entry.path,
                entry.identity_id,
                entry.status,
                entry.created_at,
                entry.updated_at,
            ),
        )

        return entry

    def get(
        self,
        entity_id: str,
    ) -> Optional[RegistryEntry]:
        """Return one registry entry."""

        row = self.database.fetch_one(
            f"""
            SELECT
                entity_id,
                entity_type,
                path,
                identity_id,
                status,
                created_at,
                updated_at
            FROM {self.TABLE_NAME}
            WHERE entity_id = ?
            """,
            (entity_id,),
        )

        if row is None:
            return None

        return RegistryEntry(
            entity_id=row["entity_id"],
            entity_type=row["entity_type"],
            path=row["path"],
            identity_id=row["identity_id"],
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def require(
        self,
        entity_id: str,
    ) -> RegistryEntry:
        """Return an entry or raise KeyError."""

        entry = self.get(entity_id)

        if entry is None:
            raise KeyError(
                f"Entity not found: {entity_id}"
            )

        return entry

    def update_path(
        self,
        entity_id: str,
        path: str,
    ) -> RegistryEntry:
        """Update an entity's filesystem path."""

        entry = self.require(entity_id)

        updated_at = datetime.now(
            timezone.utc
        ).isoformat()

        self.database.execute(
            f"""
            UPDATE {self.TABLE_NAME}
            SET
                path = ?,
                updated_at = ?
            WHERE entity_id = ?
            """,
            (
                path,
                updated_at,
                entity_id,
            ),
        )

        entry.path = path
        entry.updated_at = updated_at

        return entry

    def update(
        self,
        entity_id: str,
        **changes,
    ) -> RegistryEntry:
        """Update allowed registry metadata."""

        entry = self.require(entity_id)

        allowed_fields = {
            "entity_type",
            "path",
            "identity_id",
            "status",
        }

        unknown_fields = (
            set(changes.keys()) - allowed_fields
        )

        if unknown_fields:
            raise ValueError(
                f"Unknown registry fields: "
                f"{sorted(unknown_fields)}"
            )

        if not changes:
            return entry

        updated_at = datetime.now(
            timezone.utc
        ).isoformat()

        assignments = []
        parameters = []

        for field in allowed_fields:
            if field in changes:
                assignments.append(
                    f"{field} = ?"
                )
                parameters.append(
                    changes[field]
                )

                setattr(
                    entry,
                    field,
                    changes[field],
                )

        assignments.append(
            "updated_at = ?"
        )
        parameters.append(updated_at)

        parameters.append(entity_id)

        self.database.execute(
            f"""
            UPDATE {self.TABLE_NAME}
            SET {", ".join(assignments)}
            WHERE entity_id = ?
            """,
            tuple(parameters),
        )

        entry.updated_at = updated_at

        return entry

    def remove(
        self,
        entity_id: str,
    ) -> bool:
        """Remove an entity from the registry."""

        self.require(entity_id)

        self.database.execute(
            f"""
            DELETE FROM {self.TABLE_NAME}
            WHERE entity_id = ?
            """,
            (entity_id,),
        )

        return True

    def find_by_path(
        self,
        path: str,
    ) -> Optional[RegistryEntry]:
        """Find an entity by filesystem path."""

        row = self.database.fetch_one(
            f"""
            SELECT
                entity_id,
                entity_type,
                path,
                identity_id,
                status,
                created_at,
                updated_at
            FROM {self.TABLE_NAME}
            WHERE path = ?
            """,
            (path,),
        )

        if row is None:
            return None

        return RegistryEntry(
            entity_id=row["entity_id"],
            entity_type=row["entity_type"],
            path=row["path"],
            identity_id=row["identity_id"],
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def list_all(self) -> list[dict]:
        """Return every registered entity."""

        rows = self.database.fetch_all(
            f"""
            SELECT
                entity_id,
                entity_type,
                path,
                identity_id,
                status,
                created_at,
                updated_at
            FROM {self.TABLE_NAME}
            ORDER BY path COLLATE NOCASE
            """
        )

        return [
            {
                "entity_id": row["entity_id"],
                "entity_type": row["entity_type"],
                "path": row["path"],
                "identity_id": row["identity_id"],
                "status": row["status"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
            for row in rows
        ]

    def count(self) -> int:
        """Return the number of registered entities."""

        row = self.database.fetch_one(
            f"""
            SELECT COUNT(*) AS total
            FROM {self.TABLE_NAME}
            """
        )

        return int(row["total"])

    def clear(self) -> None:
        """
        Clear the registry.

        Intended for controlled maintenance/testing operations.
        """

        self.database.execute(
            f"""
            DELETE FROM {self.TABLE_NAME}
            """
        )


registry = FoundationRegistry()


__all__ = [
    "RegistryEntry",
    "FoundationRegistry",
    "registry",
]
