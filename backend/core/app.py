from backend.config.service import ConfigService
from backend.identity.service import IdentityService
from backend.auth.service import AuthenticationService
from backend.database.service import DatabaseService
from backend.storage.service import StorageService
from backend.security.service import SecurityService
from backend.api.service import APIService


class MainBaseFoundation:

    def __init__(self):
        self.config = ConfigService()
        self.identity = IdentityService()
        self.authentication = AuthenticationService()
        self.database = DatabaseService()
        self.storage = StorageService()
        self.security = SecurityService()
        self.api = APIService()

    def start(self):
        return "MAIN BASE FOUNDATION STARTED"
