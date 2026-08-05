from backend.roles.service import RoleService


class RoleController:

    def __init__(self):
        self.service = RoleService()

    def initialize(self):
        return self.service.initialize()

    def create(self, **kwargs):
        role = self.service.create_role(**kwargs)
        self.service.save_role(role)
        return role

    def get(self, role_id):
        return self.service.get_role(role_id)

    def update(self, **kwargs):
        self.service.update_role(**kwargs)

    def delete(self, role_id):
        self.service.delete_role(role_id)

    def list(self):
        return self.service.get_all_roles()

    def search(self, role_name):
        return self.service.search_role_by_name(role_name)
