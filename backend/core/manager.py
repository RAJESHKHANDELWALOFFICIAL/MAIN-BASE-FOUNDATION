from backend.core.app import MainBaseFoundation
from backend.core.bootstrap import Bootstrap


class FoundationManager:

    def __init__(self):
        self.bootstrap = Bootstrap()
        self.foundation = MainBaseFoundation()

    def start(self):
        boot = self.bootstrap.boot()
        system = self.foundation.start()

        return {
            "boot": boot,
            "system": system
        }
