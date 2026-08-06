from backend.identity.controller import IdentityController


class IdentityManager:

    def __init__(self):

        self.controller = IdentityController()

    def initialize(self):
        return self.controller.initialize()

    def create(self, **kwargs):
        return self.controller.create(**kwargs)

    def get(self, master_id):
        return self.controller.get(master_id)

    def list(self):
        return self.controller.list()
