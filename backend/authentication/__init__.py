"""MAIN BASE FOUNDATION authentication package.

Public interface for the authentication layer.
"""

from .manager import AuthenticationManager
from .models import Credential


__all__ = [
    "AuthenticationManager",
    "Credential",
]
