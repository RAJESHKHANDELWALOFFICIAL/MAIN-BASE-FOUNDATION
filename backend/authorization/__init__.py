"""MAIN BASE FOUNDATION authorization system."""

from .manager import AuthorizationManager
from .models import AuthorizationRequest

__all__ = [
    "AuthorizationManager",
    "AuthorizationRequest",
]
