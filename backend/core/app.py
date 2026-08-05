from backend.logger.service import LoggerService
from backend.config.service import ConfigService
from backend.database.service import DatabaseService
from backend.identity.service import IdentityService
from backend.auth.service import AuthenticationService
from backend.status.service import StatusService
from backend.storage.service import StorageService
from backend.security.service import SecurityService
from backend.api.service import APIService
from backend.users.service import UserService


class MainBaseFoundation:

    def __init__(self):
        self.logger = LoggerService()

        self.config = ConfigService()
        self.database = DatabaseService()
        self.identity = IdentityService()
        self.authentication = AuthenticationService()
        self.status = StatusService()
        self.storage = StorageService()
        self.security = SecurityService()
        self.api = APIService()
        self.users = UserService()

    def start(self):

        self.logger.info(
            "CORE",
            "MAIN BASE FOUNDATION boot started."
        )

        config = self.config.initialize()
        database = self.database.initialize()
        identity = self.identity.initialize()
        authentication = self.authentication.initialize()
        status = self.status.initialize()
        storage = self.storage.initialize()
        security = self.security.initialize()
        api = self.api.initialize()
        users = self.users.initialize()

        self.logger.info(
            "CORE",
            "MAIN BASE FOUNDATION boot completed successfully."
        )

        return {
            "config": config,
            "database": database,
            "identity": {
                "master_id": identity.master_id,
                "full_name": identity.full_name,
                "username": identity.primary_username,
                "status": identity.status,
            },
            "authentication": authentication,
            "status": status,
            "storage": storage,
            "security": security,
            "api": api,
            "users": users,
        }
