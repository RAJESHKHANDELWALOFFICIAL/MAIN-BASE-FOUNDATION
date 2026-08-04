from dataclasses import dataclass


@dataclass
class StorageInfo:
    storage_name: str
    version: str
    status: str = "Connected"
