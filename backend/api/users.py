from fastapi import APIRouter
from backend.users.controller import UserController

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

controller = UserController()


@router.get("/")
def get_users():
    return controller.list()


@router.get("/{user_id}")
def get_user(user_id: str):
    return controller.get(user_id)


@router.post("/")
def create_user():

    user = controller.register(
        user_id="USR-000001",
        full_name="DR RAJESH KHANDELWAL IBC",
        username="RAJESHKHANDELWALOFFICIAL",
        email="demo@example.com",
        phone="+910000000000",
        password="123456",
        role="ADMIN",
        status="ACTIVE"
    )

    return user


@router.put("/{user_id}")
def update_user(user_id: str):

    controller.update(
        user_id=user_id,
        full_name="Updated User",
        username="updateduser",
        email="updated@example.com",
        phone="+911111111111",
        password="654321",
        role="ADMIN",
        status="ACTIVE"
    )

    return {
        "message": "User updated successfully"
    }


@router.delete("/{user_id}")
def delete_user(user_id: str):

    controller.delete(user_id)

    return {
        "message": "User deleted successfully"
    }
