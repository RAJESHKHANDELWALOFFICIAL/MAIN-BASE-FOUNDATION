from fastapi import APIRouter

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def dashboard():
    return {
        "message": "Dashboard API Working"
    }


@router.get("/summary")
def summary():
    return {
        "message": "Dashboard Summary"
    }


@router.get("/statistics")
def statistics():
    return {
        "message": "Dashboard Statistics"
    }


@router.get("/health")
def health():
    return {
        "message": "Dashboard Health"
    }


@router.get("/version")
def version():
    return {
        "version": "1.0.0"
    }
