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

    def update(self, identity):
        return self.controller.update(identity)

    def delete(self, master_id):
        return self.controller.delete(master_id)

    def search(self, keyword):
        return self.controller.search(keyword)

    def verify(self, master_id):
        return self.controller.verify(master_id)

    def exists(self, master_id):
        return self.controller.exists(master_id)
