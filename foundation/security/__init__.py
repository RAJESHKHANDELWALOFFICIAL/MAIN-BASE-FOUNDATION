"""
MAIN BASE FOUNDATION
Security Package
"""

from foundation.security.access import (
    AccessController,
    AccessDeniedError,
    access_controller,
)

__all__ = [
    "AccessController",
    "AccessDeniedError",
    "access_controller",
]
