from dataclasses import dataclass


@dataclass
class APIInfo:
    api_name: str
    version: str
    status: str = "Available"
  
