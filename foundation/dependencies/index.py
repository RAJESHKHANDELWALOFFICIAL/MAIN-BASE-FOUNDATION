"""
MAIN BASE FOUNDATION
Persistent Dependency and Reference Index

Maintains controlled relationships between entities.
"""

from dataclasses import dataclass
from typing import Optional

from backend.engines.database.manager import DatabaseEngine


@dataclass
class Dependency:
    source_id: str
    target_id: str
    relationship: str

    def to_dict(self) -> dict:
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relationship": self.relationship,
        }


class DependencyIndex:

    TABLE_NAME = "foundation_dependencies"

    def __init__(
        self,
        database: Optional[DatabaseEngine] = None,
    ):
        self.database = (
            database or DatabaseEngine()
        )
        self._initialize()

    def _initialize(self) -> None:
        self.database.create_table(
            f"""
            CREATE TABLE IF NOT EXISTS
            {self.TABLE_NAME} (
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

    def add(
        self,
        source_id: str,
        target_id: str,
        relationship: str,
    ) -> Dependency:

        if not source_id:
            raise ValueError(
                "source_id cannot be empty."
            )

        if not target_id:
            raise ValueError(
                "target_id cannot be empty."
            )

        if not relationship:
            raise ValueError(
                "relationship cannot be empty."
            )

        dependency = Dependency(
            source_id=source_id,
            target_id=target_id,
            relationship=relationship,
        )

        self.database.execute(
            f"""
            INSERT OR IGNORE INTO
            {self.TABLE_NAME} (
                source_id,
                target_id,
                relationship
            )
            VALUES (?, ?, ?)
            """,
            (
                source_id,
                target_id,
                relationship,
            ),
        )

        return dependency

    def exists(
        self,
        source_id: str,
        target_id: str,
        relationship: str,
    ) -> bool:

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

    def remove(
        self,
        source_id: str,
        target_id: str,
        relationship: str,
    ) -> bool:

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

    def get_dependencies(
        self,
        source_id: str,
    ) -> list[dict]:

        rows = self.database.fetch_all(
            f"""
            SELECT
                source_id,
                target_id,
                relationship
            FROM {self.TABLE_NAME}
            WHERE source_id = ?
            ORDER BY target_id
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

    def get_dependents(
        self,
        target_id: str,
    ) -> list[dict]:

        rows = self.database.fetch_all(
            f"""
            SELECT
                source_id,
                target_id,
                relationship
            FROM {self.TABLE_NAME}
            WHERE target_id = ?
            ORDER BY source_id
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

    def get_entity_relationships(
        self,
        entity_id: str,
    ) -> list[dict]:

        rows = self.database.fetch_all(
            f"""
            SELECT
                source_id,
                target_id,
                relationship
            FROM {self.TABLE_NAME}
            WHERE source_id = ?
               OR target_id = ?
            ORDER BY relationship
            """,
            (
                entity_id,
                entity_id,
            ),
        )

        return [
            {
                "source_id": row["source_id"],
                "target_id": row["target_id"],
                "relationship": row["relationship"],
            }
            for row in rows
        ]

    def remove_entity(
        self,
        entity_id: str,
    ) -> int:
        """
        Remove every dependency where the entity
        is either the source or target.
        """

        relationships = (
            self.get_entity_relationships(
                entity_id
            )
        )

        self.database.execute(
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

        return len(relationships)

    def list_all(self) -> list[dict]:

        rows = self.database.fetch_all(
            f"""
            SELECT
                source_id,
                target_id,
                relationship
            FROM {self.TABLE_NAME}
            ORDER BY source_id, target_id
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

    def count(self) -> int:

        row = self.database.fetch_one(
            f"""
            SELECT COUNT(*) AS total
            FROM {self.TABLE_NAME}
            """
        )

        return int(row["total"])

    def clear(self) -> None:

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
