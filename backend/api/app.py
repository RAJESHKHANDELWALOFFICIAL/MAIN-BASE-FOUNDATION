from fastapi import FastAPI

from backend.api.users import router as users_router
from backend.api.businesses import router as businesses_router
from backend.api.projects import router as projects_router
from backend.api.supreme import router as supreme_router
from backend.api.identity import router as identity_router


app = FastAPI(
    title="MAIN BASE FOUNDATION API",
    version="1.0.0"
)


# ==========================
# ROUTERS
# ==========================

app.include_router(users_router)
app.include_router(businesses_router)
app.include_router(projects_router)
app.include_router(supreme_router)
app.include_router(identity_router)


# ==========================
# HOME
# ==========================

@app.get("/")
def home():

    return {
        "project": "MAIN BASE FOUNDATION",
        "version": "1.0.0",
        "status": "RUNNING"
    }
