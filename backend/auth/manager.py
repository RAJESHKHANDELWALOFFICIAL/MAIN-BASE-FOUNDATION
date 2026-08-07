from backend.auth.controller import AuthenticationController


class AuthenticationManager:

    def __init__(self):

        self.controller = AuthenticationController()

    def initialize(self):

        return self.controller.initialize()

    def authenticate(self, master_id):

        return self.controller.authenticate(master_id)

    def login(self, master_id):

        return self.controller.login(master_id)

    def logout(self):

        return self.controller.logout()
