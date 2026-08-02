from .model import MasterIdentity


class IdentityService:

    def create_demo_identity(self):
        return MasterIdentity(
            master_id="MBF-000001",
            full_name="Demo User",
            display_name="Demo",
            primary_username="demo",
            email="demo@example.com",
            phone="+910000000000",
        )
