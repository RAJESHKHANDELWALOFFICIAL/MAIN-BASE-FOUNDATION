from backend.security.connection import SecurityConnection


class SecurityService:

    def __init__(self):
        self.connection = SecurityConnection()

    def initialize(self):
        return self.connection.connect()
