"""
MAIN BASE FOUNDATION
Audit and History System

Central record of foundation operations.
"""

from dataclasses import dataclass, asdict
from datetime import datetime, timezone


@dataclass
class AuditRecord:
    """
    Represents one recorded foundation operation.
    """

    operation: str
    entity_id: str
    path: str
    subject_id: str
    status: str
    details: str = ""
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = (
                datetime.now(timezone.utc).isoformat()
            )

    def to_dict(self) -> dict:
        return asdict(self)


class AuditLog:
    """
    Central in-memory audit history.
    """

    def __init__(self):
        self._records: list[AuditRecord] = []

    def record(
        self,
        operation: str,
        entity_id: str,
        path: str,
        subject_id: str,
        status: str,
        details: str = "",
    ) -> AuditRecord:

        record = AuditRecord(
            operation=operation,
            entity_id=entity_id,
            path=path,
            subject_id=subject_id,
            status=status,
            details=details,
        )

        self._records.append(record)

        return record

    def list_all(self) -> list[dict]:
        return [
            record.to_dict()
            for record in self._records
        ]

    def get_entity_history(
        self,
        entity_id: str,
    ) -> list[dict]:

        return [
            record.to_dict()
            for record in self._records
            if record.entity_id == entity_id
        ]

    def get_subject_history(
        self,
        subject_id: str,
    ) -> list[dict]:

        return [
            record.to_dict()
            for record in self._records
            if record.subject_id == subject_id
        ]

    def clear(self) -> None:
        self._records.clear()


audit_log = AuditLog()


__all__ = [
    "AuditRecord",
    "AuditLog",
    "audit_log",
]
