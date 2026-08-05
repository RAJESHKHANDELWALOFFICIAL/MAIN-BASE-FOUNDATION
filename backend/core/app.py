def start(self):

    self.logger.info(
        "CORE",
        "MAIN BASE FOUNDATION boot started."
    )

    config = self.config.initialize()
    database = self.database.initialize()
    identity = self.identity.initialize()
    authentication = self.authentication.initialize()
    status = self.status.initialize()

    self.logger.info(
        "CORE",
        "MAIN BASE FOUNDATION boot completed successfully."
    )

    return {
        "config": config,
        "database": database,
        "identity": {
            "master_id": identity.master_id,
            "full_name": identity.full_name,
            "username": identity.primary_username,
            "status": identity.status,
        },
        "authentication": authentication,
        "status": status,
    }
