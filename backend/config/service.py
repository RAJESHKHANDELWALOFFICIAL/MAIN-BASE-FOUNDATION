def initialize(self):
    return {
        "app_name": self.get_app_name(),
        "version": self.get_version(),
        "status": self.get_status()
    }
