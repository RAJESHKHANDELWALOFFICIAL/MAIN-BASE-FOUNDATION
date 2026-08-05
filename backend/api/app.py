from fastapi import FastAPI

from backend.api.users import router as users_router
from backend.api.businesses import router as businesses_router
from backend.api.projects import router as projects_router

app = FastAPI(
    title="MAIN BASE FOUNDATION API",
    version="1.0.0"
)

app.include_router(users_router)
app.include_router(businesses_router)
app.include_router(projects_router)


@app.get("/")
def home():
    return {
        "project": "MAIN BASE FOUNDATION"
    }
