from backend.auth.service import AuthenticationService


class AuthenticationController:

    def __init__(self):

        self.service = AuthenticationService()

    def initialize(self):

        return self.service.initialize()

    def authenticate(self, master_id):

        return self.service.authenticate(master_id)

    def login(self, master_id):

        return self.service.login(master_id)

    def logout(self):

        return self.service.logout()
