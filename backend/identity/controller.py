from backend.identity.service import IdentityService


class IdentityController:

    def __init__(self):

        self.service = IdentityService()
    def initialize(self):
        return self.service.initialize()

    def create(self, **kwargs):
        identity = self.service.create_identity(**kwargs)
        self.service.save_identity(identity)
        return identity

    def get(self, master_id):
        return self.service.get_identity(master_id)

    def list(self):
        return self.service.list_identity()
        
