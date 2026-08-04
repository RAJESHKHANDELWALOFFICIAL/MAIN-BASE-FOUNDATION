from backend.config.service import ConfigService
from backend.identity.service import IdentityService
from backend.auth.service import AuthenticationService


class CoreService:

    def __init__(self):
        self.config = ConfigService()
        self.identity = IdentityService()
        self.auth = AuthenticationService()

    def initialize(self):
        return {
            "config": "Ready",
            "identity": "Ready",
            "authentication": "Ready"
        }
