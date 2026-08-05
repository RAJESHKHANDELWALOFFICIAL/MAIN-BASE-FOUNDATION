def __init__(self):
    self.logger = LoggerService()

    self.config = ConfigService()
    self.database = DatabaseService()
    self.identity = IdentityService()
    self.authentication = AuthenticationService()
