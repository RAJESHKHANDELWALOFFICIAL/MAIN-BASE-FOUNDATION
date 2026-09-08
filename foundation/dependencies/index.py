"""
MAIN BASE FOUNDATION
Persistent Dependency and Reference Index

Maintains controlled relationships between
entities inside MAIN-BASE-FOUNDATION.
"""

from dataclasses import dataclass
from typing import Optional

from backend.engines.database.manager import DatabaseEngine


@dataclass
class Dependency:
    """
    Represents one directed relationship between
    two foundation entities.
    """

    source_id: str
    target_id: str
    relationship: str

    def __post_init__(self):
        if not self.source_id:
            raise ValueError("source_id is required.")

        if not self.target_id:
            raise ValueError("target_id is required.")

        if not self.relationship:
            raise ValueError("relationship is required.")

    def to_dict(self) -> dict:
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relationship": self.relationship,
        }


class DependencyIndex:
    """
    Persistent central dependency and reference manager.

    Relationships survive process restarts and are stored
    in the central MAIN-BASE-FOUNDATION database.
    """

    TABLE_NAME = "foundation_dependencies"

    def __init__(
        self,
        database: Optional[DatabaseEngine] = None,
    ):
        self.database = database or DatabaseEngine()
        self._initialize()

    # ==========================================================
    # DATABASE INITIALIZATION
    # ==========================================================

    def _initialize(self) -> None:
        """Create dependency storage when required."""

        self.database.create_table(
            f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                source_id TEXT NOT NULL,
                target_id TEXT NOT NULL,
                relationship TEXT NOT NULL,
                PRIMARY KEY (
                    source_id,
                    target_id,
                    relationship
                )
            )
            """
        )

        self.database.execute(
            f"""
            CREATE INDEX IF NOT EXISTS
            idx_{self.TABLE_NAME}_source
            ON {self.TABLE_NAME}(source_id)
            """
        )

        self.database.execute(
            f"""
            CREATE INDEX IF NOT EXISTS
            idx_{self.TABLE_NAME}_target
            ON {self.TABLE_NAME}(target_id)
            """
        )

    # ==========================================================
    # ADD
    # ==========================================================

    def add(
        self,
        source_id: str,
        target_id: str,
        relationship: str,
    ) -> Dependency:
        """Persist a new dependency relationship."""

        dependency = Dependency(
            source_id=source_id,
            target_id=target_id,
            relationship=relationship,
        )

        if self.exists(
            source_id,
            target_id,
            relationship,
        ):
            raise ValueError(
                "Dependency already exists."
            )

        self.database.execute(
            f"""
            INSERT INTO {self.TABLE_NAME} (
                source_id,
                target_id,
                relationship
            )
            VALUES (?, ?, ?)
            """,
            (
                dependency.source_id,
                dependency.target_id,
                dependency.relationship,
            ),
        )

        return dependency

    # ==========================================================
    # EXISTS
    # ==========================================================

    def exists(
        self,
        source_id: str,
        target_id: str,
        relationship: str,
    ) -> bool:
        """Check whether a relationship exists."""

        row = self.database.fetch_one(
            f"""
            SELECT 1
            FROM {self.TABLE_NAME}
            WHERE source_id = ?
              AND target_id = ?
              AND relationship = ?
            LIMIT 1
            """,
            (
                source_id,
                target_id,
                relationship,
            ),
        )

        return row is not None

    # ==========================================================
    # REMOVE
    # ==========================================================

    def remove(
        self,
        source_id: str,
        target_id: str,
        relationship: str,
    ) -> bool:
        """Remove one dependency relationship."""

        if not self.exists(
            source_id,
            target_id,
            relationship,
        ):
            raise KeyError(
                "Dependency not found."
            )

        self.database.execute(
            f"""
            DELETE FROM {self.TABLE_NAME}
            WHERE source_id = ?
              AND target_id = ?
              AND relationship = ?
            """,
            (
                source_id,
                target_id,
                relationship,
            ),
        )

        return True

    # ==========================================================
    # SOURCE DEPENDENCIES
    # ==========================================================

    def get_dependencies(
        self,
        source_id: str,
    ) -> list[dict]:
        """
        Return all entities that the source depends on.
        """

        rows = self.database.fetch_all(
            f"""
            SELECT
                source_id,
                target_id,
                relationship
            FROM {self.TABLE_NAME}
            WHERE source_id = ?
            ORDER BY target_id COLLATE NOCASE
            """,
            (source_id,),
        )

        return [
            {
                "source_id": row["source_id"],
                "target_id": row["target_id"],
                "relationship": row["relationship"],
            }
            for row in rows
        ]

    # ==========================================================
    # TARGET DEPENDENTS
    # ==========================================================

    def get_dependents(
        self,
        target_id: str,
    ) -> list[dict]:
        """
        Return all entities that depend on the target.
        """

        rows = self.database.fetch_all(
            f"""
            SELECT
                source_id,
                target_id,
                relationship
            FROM {self.TABLE_NAME}
            WHERE target_id = ?
            ORDER BY source_id COLLATE NOCASE
            """,
            (target_id,),
        )

        return [
            {
                "source_id": row["source_id"],
                "target_id": row["target_id"],
                "relationship": row["relationship"],
            }
            for row in rows
        ]

    # ==========================================================
    # ENTITY RELATIONSHIPS
    # ==========================================================

    def get_entity_relationships(
        self,
        entity_id: str,
    ) -> dict:
        """
        Return both outgoing and incoming relationships
        for one entity.
        """

        return {
            "entity_id": entity_id,
            "dependencies": self.get_dependencies(
                entity_id
            ),
            "dependents": self.get_dependents(
                entity_id
            ),
        }

    # ==========================================================
    # REMOVE ENTITY RELATIONSHIPS
    # ==========================================================

    def remove_entity(
        self,
        entity_id: str,
    ) -> int:
        """
        Remove every relationship connected to an entity.

        This is used when an entity is permanently removed
        from the foundation.
        """

        result = self.database.execute(
            f"""
            DELETE FROM {self.TABLE_NAME}
            WHERE source_id = ?
               OR target_id = ?
            """,
            (
                entity_id,
                entity_id,
            ),
        )

        return result.rowcount

    # ==========================================================
    # LIST ALL
    # ==========================================================

    def list_all(self) -> list[dict]:
        """Return every dependency relationship."""

        rows = self.database.fetch_all(
            f"""
            SELECT
                source_id,
                target_id,
                relationship
            FROM {self.TABLE_NAME}
            ORDER BY
                source_id COLLATE NOCASE,
                target_id COLLATE NOCASE,
                relationship COLLATE NOCASE
            """
        )

        return [
            {
                "source_id": row["source_id"],
                "target_id": row["target_id"],
                "relationship": row["relationship"],
            }
            for row in rows
        ]

    # ==========================================================
    # COUNT
    # ==========================================================

    def count(self) -> int:
        """Return total dependency relationships."""

        row = self.database.fetch_one(
            f"""
            SELECT COUNT(*) AS total
            FROM {self.TABLE_NAME}
            """
        )

        return int(
            row["total"]
        )

    # ==========================================================
    # CLEAR
    # ==========================================================

    def clear(self) -> None:
        """
        Clear all dependency relationships.

        Intended only for controlled maintenance/testing.
        """

        self.database.execute(
            f"""
            DELETE FROM {self.TABLE_NAME}
            """
        )


dependency_index = DependencyIndex()


__all__ = [
    "Dependency",
    "DependencyIndex",
    "dependency_index",
]
