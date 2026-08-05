from fastapi import APIRouter

router = APIRouter(
    prefix="/businesses",
    tags=["Businesses"]
)


@router.get("/")
def get_businesses():
    return {
        "message": "Businesses API Working"
    }
