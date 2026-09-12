from backend.auth.service import AuthenticationService


class AuthenticationController:

    def __init__(self):

        self.service = AuthenticationService()

    def initialize(self):

        return self.service.initialize()

    def authenticate(self, master_id):

        return self.service.authenticate(
            master_id
        )

    def login(
        self,
        master_id=None,
        username=None,
        password=None
    ):

        return self.service.login(
            master_id=master_id,
            username=username,
            password=password
        )

    def logout(self):

        return self.service.logout()
