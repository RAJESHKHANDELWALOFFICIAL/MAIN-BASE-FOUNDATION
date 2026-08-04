from backend.identity.model import MasterIdentity


class IdentityService:

    def create_identity(
        self,
        master_id,
        full_name,
        display_name,
        username,
        email,
        phone,
    ):
        return MasterIdentity(
            master_id=master_id,
            full_name=full_name,
            display_name=display_name,
            primary_username=username,
            email=email,
            phone=phone,
        )

    def initialize(self):
        return self.create_identity(
            master_id="MBF-000001",
            full_name="DR RAJESH KHANDELWAL IBC",
            display_name="DR RAJESH KHANDELWAL IBC",
            username="RAJESHKHANDELWALOFFICIAL",
            email="demo@example.com",
            phone="+910000000000",
        )
