from backend.config.service import ConfigService
from backend.identity.service import IdentityService


class MainBaseFoundation:

    def __init__(self):
        self.config = ConfigService()
        self.identity = IdentityService()

    def start(self):
        return "MAIN BASE FOUNDATION STARTED"
