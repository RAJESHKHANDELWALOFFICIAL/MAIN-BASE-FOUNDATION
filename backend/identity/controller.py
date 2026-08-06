from backend.identity.service import IdentityService


class IdentityController:

    def __init__(self):

        self.service = IdentityService()
