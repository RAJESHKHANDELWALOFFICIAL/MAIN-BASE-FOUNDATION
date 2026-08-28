"""Provider integration definitions."""

from .google import GOOGLE
from .microsoft import MICROSOFT
from .aws import AWS
from .apple import APPLE
from .github import GITHUB
from .cloudflare import CLOUDFLARE

__all__ = [
    "GOOGLE",
    "MICROSOFT",
    "AWS",
    "APPLE",
    "GITHUB",
    "CLOUDFLARE",
]
