from backend.supreme.service import SupremeService


class SupremeController:

    def __init__(self):
        self.service = SupremeService()

    def initialize(self):
        return self.service.initialize()

    def create(self, **kwargs):
        owner = self.service.create_owner(**kwargs)
        self.service.save_owner(owner)
        return owner

    def get(self):
        return self.service.get_owner()

    def update(self, owner):
        self.service.update_owner(owner)

    def delete(self, supreme_id):
        self.service.delete_owner(supreme_id)

    def list(self):
        return self.service.list_owner()

    def exists(self):
        return self.service.owner_exists()

    def login(self, identifier):
        return self.service.login(identifier)

    def logout(self):
        return self.service.logout()

    def change_password(self, supreme_id, password):
        return self.service.change_password(
            supreme_id,
            password
        )
