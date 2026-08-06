from fastapi import APIRouter

from backend.supreme.controller import SupremeController


router = APIRouter(
    prefix="/supreme",
    tags=["Supreme"]
)

controller = SupremeController()


@router.get("/")
def get_owner():
    return controller.get()


@router.post("/")
def create_owner():

    owner = controller.create(
        master_id="MBF-000001",
        supreme_id="SUP-000001",
        owner_name="DR RAJESH KHANDELWAL IBC",
        username="RAJESHKHANDELWALOFFICIAL",
        email="demo@example.com",
        phone="+910000000000",
        password="123456"
    )

    return {
        "message": "Supreme Owner Created Successfully",
        "data": owner
    }


@router.put("/{supreme_id}")
def update_owner(supreme_id: str):

    return {
        "message": "Update API Coming Soon",
        "supreme_id": supreme_id
    }


@router.delete("/{supreme_id}")
def delete_owner(supreme_id: str):

    controller.delete(supreme_id)

    return {
        "message": "Supreme Owner Deleted Successfully"
    }


@router.get("/list")
def list_owner():
    return controller.list()


@router.post("/login")
def login(identifier: str):
    return controller.login(identifier)


@router.post("/logout")
def logout():
    return controller.logout()


@router.put("/change-password")
def change_password(
    supreme_id: str,
    password: str
):
    return controller.change_password(
        supreme_id,
        password
    )
