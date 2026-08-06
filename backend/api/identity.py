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

@router.put("/{master_id}")
def update_identity(master_id: str):

    return {
        "message": "Update API Coming Soon",
        "master_id": master_id
    }


@router.delete("/{master_id}")
def delete_identity(master_id: str):

    controller.delete(master_id)

    return {
        "message": "Identity Deleted Successfully"
    }


@router.get("/search")
def search_identity(keyword: str):

    return controller.search(keyword)


@router.put("/verify/{master_id}")
def verify_identity(master_id: str):

    return controller.verify(master_id)


@router.get("/exists/{master_id}")
def identity_exists(master_id: str):

    return {
        "exists": controller.exists(master_id)
    }
