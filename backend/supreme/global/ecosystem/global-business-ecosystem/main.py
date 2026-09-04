"""
Global Business Ecosystem
Runtime Entry Point
"""

from fastapi import FastAPI

from api.routes import router as api_router

from config.settings import settings


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)


app.include_router(
    api_router,
    prefix="/api"
)


@app.get("/")
def root():
    return {
        "system": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "active"
    }
