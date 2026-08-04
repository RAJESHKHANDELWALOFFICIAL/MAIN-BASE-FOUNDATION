
from dataclasses import dataclass


@dataclass
class DatabaseInfo:
    database_name: str
    version: str
    status: str = "Connected"
