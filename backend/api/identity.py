from fastapi import APIRouter

from backend.identity.controller import IdentityController


router = APIRouter(
    prefix="/identity",
    tags=["Identity"]
)

controller = IdentityController()
