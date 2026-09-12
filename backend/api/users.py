from fastapi import APIRouter
from backend.users.controller import UserController

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

controller = UserController()


@router.get("/")
def get_users():
    users = controller.list()

    return {
        "message": "Users retrieved successfully",
        "data": [user.to_dict() for user in users]
    }


@router.get("/{user_id}")
def get_user(user_id: str):
    user = controller.get(user_id)

    if user is None:
        return {
            "message": "User not found",
            "data": None
        }

    return {
        "message": "User retrieved successfully",
        "data": user.to_dict()
    }


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

    return {
        "message": "User created successfully",
        "data": user.to_dict()
    }


@router.put("/{user_id}")
def update_user(user_id: str):
    user = controller.update(
        user_id=user_id,
        full_name="Updated User",
        username="updateduser",
        email="updated@example.com",
        phone="+911111111111",
        password="654321",
        role="ADMIN",
        status="ACTIVE"
    )

    if user is None:
        return {
            "message": "User not found",
            "data": None
        }

    return {
        "message": "User updated successfully",
        "data": user.to_dict()
    }


@router.delete("/{user_id}")
def delete_user(user_id: str):
    result = controller.delete(user_id)

    return {
        "message": "User deleted successfully",
        "data": result
    }
