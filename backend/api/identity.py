from fastapi import APIRouter

from backend.identity.controller import IdentityController


router = APIRouter(
    prefix="/identity",
    tags=["Identity"]
)

controller = IdentityController()

@router.get("/")
def get_identity(master_id: str):
    return controller.get(master_id)


@router.post("/")
def create_identity():

    identity = controller.create(
        supreme_id="SUP-000001",
        full_name="DR RAJESH KHANDELWAL IBC",
        display_name="DR RAJESH KHANDELWAL IBC",
        username="RAJESHKHANDELWALOFFICIAL",
        email="demo@example.com",
        phone="910000000000"
    )

    return {
        "message": "Identity Created Successfully",
        "data": identity
    }


@router.get("/list")
def list_identity():
    return controller.list()
