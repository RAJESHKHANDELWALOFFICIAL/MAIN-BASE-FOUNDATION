def create(
    self,
    organization_id: str,
    organization_name: str,
    organization_type: str,
    operating_model: str,
    country: str,
    region: str,
    owner_id: str | None = None,
    facility_type: str | None = None,
    description: str | None = None,
) -> dict:
    """Create an organization."""

    if organization_id in self.organizations:
        return {
            "success": False,
            "error": "ORGANIZATION_ID_ALREADY_EXISTS",
            "organization_id": organization_id,
        }

    organization = Organization(
        organization_id=organization_id,
        organization_name=organization_name,
        organization_type=organization_type,
        operating_model=operating_model,
        country=country,
        region=region,
        owner_id=owner_id,
        facility_type=facility_type,
        description=description,
    )

    self.organizations[
        organization_id
    ] = organization

    return {
        "success": True,
        "organization": organization.__dict__,
    }
