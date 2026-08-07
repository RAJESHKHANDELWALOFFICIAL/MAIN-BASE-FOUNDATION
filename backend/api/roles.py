from fastapi import APIRouter

from backend.roles.controller import RoleController


router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

controller = RoleController()


@router.get("/")
def get_roles():
    return controller.list()


@router.get("/{role_id}")
def get_role(role_id: str):
    return controller.get(role_id)


@router.post("/")
def create_role():

    role = controller.create(
        role_id="ROLE-000001",
        role_name="ADMIN",
        description="System Administrator",
        level=1,
        status="ACTIVE"
    )

    return {
        "message": "Role Created Successfully",
        "data": role
    }


@router.put("/{role_id}")
def update_role(role_id: str):

    controller.update(
        role_id=role_id,
        role_name="SUPER ADMIN",
        description="Updated System Administrator",
        level=1,
        status="ACTIVE"
    )

    return {
        "message": "Role Updated Successfully"
    }


@router.delete("/{role_id}")
def delete_role(role_id: str):

    controller.delete(role_id)

    return {
        "message": "Role Deleted Successfully"
    }
