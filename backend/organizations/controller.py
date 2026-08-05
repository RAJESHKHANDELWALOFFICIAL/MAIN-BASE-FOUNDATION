from backend.organizations.service import OrganizationService


class OrganizationController:

    def __init__(self):
        self.service = OrganizationService()

    def initialize(self):
        return self.service.initialize()

    def create(self, **kwargs):
        return self.service.create_organization(**kwargs)
