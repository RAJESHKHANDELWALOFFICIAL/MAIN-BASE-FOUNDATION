from backend.api.connection import APIConnection


class APIService:

    def __init__(self):
        self.connection = APIConnection()

    def initialize(self):
        return self.connection.connect()
