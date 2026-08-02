from .model import MasterIdentity


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
