from fastapi import APIRouter

from backend.auth.controller import AuthenticationController


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

controller = AuthenticationController()


@router.get("/initialize")
def initialize():

    return controller.initialize()


@router.post("/login")
def login(master_id: str):

    return controller.login(master_id)


@router.post("/authenticate")
def authenticate(master_id: str):

    return controller.authenticate(master_id)


@router.post("/logout")
def logout():

    return controller.logout()
