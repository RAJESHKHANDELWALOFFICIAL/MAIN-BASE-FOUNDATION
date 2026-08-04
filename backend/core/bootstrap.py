from backend.config.service import ConfigService
from backend.identity.service import IdentityService
from backend.auth.service import AuthenticationService


class Bootstrap:

    def boot(self):
        config = ConfigService()
        identity = IdentityService()
        auth = AuthenticationService()

        return {
            "config": "Ready",
            "identity": "Ready",
            "authentication": "Ready",
            "system": "MAIN BASE FOUNDATION BOOTED"
        }
