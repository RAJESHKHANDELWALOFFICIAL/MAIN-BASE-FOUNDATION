from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class DatabaseInfo:

    id: Optional[int] = None

    database_name: str = "main_base_foundation.db"

    database_type: str = "SQLite"

    version: str = "1.0.0"

    status: str = "CONNECTED"

    foundation: str = "MAIN BASE FOUNDATION"

    created_at: str = datetime.utcnow().isoformat()

    updated_at: str = datetime.utcnow().isoformat()
