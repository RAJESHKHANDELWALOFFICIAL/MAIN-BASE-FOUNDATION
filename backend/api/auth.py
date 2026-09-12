from fastapi import APIRouter
from pydantic import BaseModel

from backend.auth.controller import AuthenticationController


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


controller = AuthenticationController()


class LoginRequest(BaseModel):

    username: str | None = None
    password: str | None = None
    master_id: str | None = None


class TokenRequest(BaseModel):

    token: str | None = None
    session_id: str | None = None


@router.get("/initialize")
def initialize():

    result = controller.initialize()

    if hasattr(result, "to_dict"):

        return result.to_dict()

    return result


@router.post("/login")
def login(
    request: LoginRequest
):

    result = controller.login(
        master_id=request.master_id,
        username=request.username,
        password=request.password
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


@router.post("/validate")
def validate_token(
    request: TokenRequest
):

    return controller.validate_token(
        request.token or ""
    )


@router.post("/logout")
def logout(
    request: TokenRequest
):

    return controller.logout(
        token=request.token,
        session_id=request.session_id
    )
