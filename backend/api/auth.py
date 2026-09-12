from fastapi import APIRouter

from backend.auth.controller import AuthenticationController


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


controller = AuthenticationController()


@router.get("/initialize")
def initialize():

    result = controller.initialize()

    if hasattr(result, "to_dict"):

        return result.to_dict()

    return result


@router.post("/login")
def login(
    username: str = None,
    password: str = None,
    master_id: str = None
):

    result = controller.login(
        master_id=master_id,
        username=username,
        password=password
    )

    if hasattr(result, "to_dict"):

        return result.to_dict()

    return result


@router.post("/authenticate")
def authenticate(
    master_id: str
):

    result = controller.authenticate(
        master_id
    )

    if hasattr(result, "to_dict"):

        return result.to_dict()

    return result


@router.post("/logout")
def logout():

    return controller.logout()
