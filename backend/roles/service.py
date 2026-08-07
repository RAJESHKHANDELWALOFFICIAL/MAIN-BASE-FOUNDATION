def create_role(
    self,
    role_id,
    role_name,
    description,
    level=1,
    status="ACTIVE"
):
    return Role(
        role_id=role_id,
        role_name=role_name,
        description=description,
        level=level,
        status=status,
    )
