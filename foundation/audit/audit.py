"""
MAIN BASE FOUNDATION
Persistent Audit and History System

Central persistent record of foundation operations.
"""

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional

from backend.engines.database.manager import DatabaseEngine


@dataclass
class AuditRecord:
    operation: str
    entity_id: str
    path: str
    subject_id: str
    status: str
    details: str = ""
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(
                timezone.utc
            ).isoformat()

    def to_dict(self) -> dict:
        return asdict(self)


class AuditLog:
    """
    Persistent audit log for MAIN-BASE-FOUNDATION.

    Every important filesystem/foundation operation can be
    recorded and retrieved after process restart.
    """

    TABLE_NAME = "foundation_audit"

    def __init__(
        self,
        database: Optional[DatabaseEngine] = None,
    ):
        self.database = database or DatabaseEngine()
        self._initialize()

    def _initialize(self) -> None:
        """Create the audit table when required."""

        self.database.create_table(
            f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation TEXT NOT NULL,
                entity_id TEXT NOT NULL,
                path TEXT NOT NULL,
                subject_id TEXT NOT NULL,
                status TEXT NOT NULL,
                details TEXT NOT NULL DEFAULT '',
                timestamp TEXT NOT NULL
            )
            """
        )

        self.database.execute(
            f"""
            CREATE INDEX IF NOT EXISTS
            idx_{self.TABLE_NAME}_entity
            ON {self.TABLE_NAME}(entity_id)
            """
        )

        self.database.execute(
            f"""
            CREATE INDEX IF NOT EXISTS
            idx_{self.TABLE_NAME}_subject
            ON {self.TABLE_NAME}(subject_id)
            """
        )

        self.database.execute(
            f"""
            CREATE INDEX IF NOT EXISTS
            idx_{self.TABLE_NAME}_timestamp
            ON {self.TABLE_NAME}(timestamp)
            """
        )

    def record(
        self,
        operation: str,
        entity_id: str,
        path: str,
        subject_id: str,
        status: str,
        details: str = "",
    ) -> AuditRecord:
        """Record a foundation operation permanently."""

        record = AuditRecord(
            operation=operation,
            entity_id=entity_id,
            path=path,
            subject_id=subject_id,
            status=status,
            details=details,
        )

        self.database.execute(
            f"""
            INSERT INTO {self.TABLE_NAME} (
                operation,
                entity_id,
                path,
                subject_id,
                status,
                details,
                timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.operation,
                record.entity_id,
                record.path,
                record.subject_id,
                record.status,
                record.details,
                record.timestamp,
            ),
        )

        return record

    def list_all(self) -> list[dict]:
        """Return all audit records."""

        rows = self.database.fetch_all(
            f"""
            SELECT
                id,
                operation,
                entity_id,
                path,
                subject_id,
                status,
                details,
                timestamp
            FROM {self.TABLE_NAME}
            ORDER BY id ASC
            """
        )

        return [
            {
                "id": row["id"],
                "operation": row["operation"],
                "entity_id": row["entity_id"],
                "path": row["path"],
                "subject_id": row["subject_id"],
                "status": row["status"],
                "details": row["details"],
                "timestamp": row["timestamp"],
            }
            for row in rows
        ]

    def get_entity_history(
        self,
        entity_id: str,
    ) -> list[dict]:
        """Return complete history for one entity."""

        rows = self.database.fetch_all(
            f"""
            SELECT
                id,
                operation,
                entity_id,
                path,
                subject_id,
                status,
                details,
                timestamp
            FROM {self.TABLE_NAME}
            WHERE entity_id = ?
            ORDER BY id ASC
            """,
            (entity_id,),
        )

        return [
            {
                "id": row["id"],
                "operation": row["operation"],
                "entity_id": row["entity_id"],
                "path": row["path"],
                "subject_id": row["subject_id"],
                "status": row["status"],
                "details": row["details"],
                "timestamp": row["timestamp"],
            }
            for row in rows
        ]

    def get_subject_history(
        self,
        subject_id: str,
    ) -> list[dict]:
        """Return complete history for one subject."""

        rows = self.database.fetch_all(
            f"""
            SELECT
                id,
                operation,
                entity_id,
                path,
                subject_id,
                status,
                details,
                timestamp
            FROM {self.TABLE_NAME}
            WHERE subject_id = ?
            ORDER BY id ASC
            """,
            (subject_id,),
        )

        return [
            {
                "id": row["id"],
                "operation": row["operation"],
                "entity_id": row["entity_id"],
                "path": row["path"],
                "subject_id": row["subject_id"],
                "status": row["status"],
                "details": row["details"],
                "timestamp": row["timestamp"],
            }
            for row in rows
        ]

    def get_operation_history(
        self,
        operation: str,
    ) -> list[dict]:
        """Return all records for one operation."""

        rows = self.database.fetch_all(
            f"""
            SELECT
                id,
                operation,
                entity_id,
                path,
                subject_id,
                status,
                details,
                timestamp
            FROM {self.TABLE_NAME}
            WHERE operation = ?
            ORDER BY id ASC
            """,
            (operation,),
        )

        return [
            {
                "id": row["id"],
                "operation": row["operation"],
                "entity_id": row["entity_id"],
                "path": row["path"],
                "subject_id": row["subject_id"],
                "status": row["status"],
                "details": row["details"],
                "timestamp": row["timestamp"],
            }
            for row in rows
        ]

    def count(self) -> int:
        """Return total number of audit records."""

        row = self.database.fetch_one(
            f"""
            SELECT COUNT(*) AS total
            FROM {self.TABLE_NAME}
            """
        )

        return int(row["total"])

    def clear(self) -> None:
        """
        Clear all audit records.

        Intended only for controlled maintenance/testing.
        """

        self.database.execute(
            f"""
            DELETE FROM {self.TABLE_NAME}
            """
        )


audit_log = AuditLog()


__all__ = [
    "AuditRecord",
    "AuditLog",
    "audit_log",
]
