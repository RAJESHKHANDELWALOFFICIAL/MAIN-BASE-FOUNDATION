from dataclasses import dataclass


@dataclass
class SecurityInfo:
    security_name: str
    version: str
    status: str = "Protected"
