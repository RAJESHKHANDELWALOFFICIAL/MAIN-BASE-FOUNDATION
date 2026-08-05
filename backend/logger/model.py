from dataclasses import dataclass
from datetime import datetime


@dataclass
class LogEntry:
    module: str
    level: str
    message: str
    created_at: str = datetime.utcnow().isoformat()
