"""MAIN BASE FOUNDATION authorization manager."""

from typing import Dict

from .models import AuthorizationRequest


class AuthorizationManager:
    """Manage authorization requests."""

    def __init__(self):
        self.requests: Dict[
            str,
            AuthorizationRequest,
        ] = {}

    def request(
        self,
        request_id: str,
        subject_id: str,
        resource: str,
        action: str,
        scope: str,
        provider_id: str | None = None,
        server_id: str | None = None,
        connection_id: str | None = None,
        reason: str | None = None,
    ) -> dict:
        """Create an authorization request."""

        if request_id in self.requests:
            return {
                "success": False,
                "error": "REQUEST_ID_ALREADY_EXISTS",
                "request_id": request_id,
            }

        authorization = AuthorizationRequest(
            request_id=request_id,
            subject_id=subject_id,
            resource=resource,
            action=action,
            scope=scope,
            provider_id=provider_id,
            server_id=server_id,
            connection_id=connection_id,
            reason=reason,
        )

        self.requests[request_id] = authorization

        return {
            "success": True,
            "authorization": authorization.__dict__,
        }

    def get(
        self,
        request_id: str,
    ) -> dict:
        """Return an authorization request."""

        authorization = self.requests.get(request_id)

        if authorization is None:
            return {
                "success": False,
                "error": "REQUEST_NOT_FOUND",
                "request_id": request_id,
            }

        return {
            "success": True,
            "authorization": authorization.__dict__,
        }

    def approve(
        self,
        request_id: str,
    ) -> dict:
        """Approve an authorization request."""

        authorization = self.requests.get(request_id)

        if authorization is None:
            return {
                "success": False,
                "error": "REQUEST_NOT_FOUND",
            }

        authorization.status = "APPROVED"

        return {
            "success": True,
            "authorization": authorization.__dict__,
        }

    def deny(
        self,
        request_id: str,
        reason: str | None = None,
    ) -> dict:
        """Deny an authorization request."""

        authorization = self.requests.get(request_id)

        if authorization is None:
            return {
                "success": False,
                "error": "REQUEST_NOT_FOUND",
            }

        authorization.status = "DENIED"

        if reason:
            authorization.reason = reason

        return {
            "success": True,
            "authorization": authorization.__dict__,
        }

    def revoke(
        self,
        request_id: str,
        reason: str | None = None,
    ) -> dict:
        """Revoke an approved authorization."""

        authorization = self.requests.get(request_id)

        if authorization is None:
            return {
                "success": False,
                "error": "REQUEST_NOT_FOUND",
            }

        authorization.status = "REVOKED"

        if reason:
            authorization.reason = reason

        return {
            "success": True,
            "authorization": authorization.__dict__,
        }

    def list(self) -> dict:
        """Return authorization requests."""

        return {
            "success": True,
            "count": len(self.requests),
            "requests": [
                request.__dict__
                for request in self.requests.values()
            ],
        }

    def health(self) -> dict:
        """Return authorization system health."""

        return {
            "system": "Authorization Manager",
            "health": "HEALTHY",
            "requests": len(self.requests),
        }
