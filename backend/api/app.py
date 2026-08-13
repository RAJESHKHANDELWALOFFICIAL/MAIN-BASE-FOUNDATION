from typing import Dict

from fastapi import FastAPI

from backend.api.users import router as users_router
from backend.api.businesses import router as businesses_router
from backend.api.projects import router as projects_router
from backend.api.supreme import router as supreme_router
from backend.api.identity import router as identity_router
from backend.api.auth import router as auth_router
from backend.api.roles import router as roles_router
from backend.api.connectivity import ConnectivityAPI


app = FastAPI(
    title="MAIN BASE FOUNDATION API",
    version="1.0.0",
)


# ==========================
# CONNECTIVITY API
# ==========================

connectivity_api = ConnectivityAPI()


# ==========================
# ROUTERS
# ==========================

app.include_router(users_router)
app.include_router(businesses_router)
app.include_router(projects_router)
app.include_router(supreme_router)
app.include_router(identity_router)
app.include_router(auth_router)
app.include_router(roles_router)


# ==========================
# CONNECTIVITY
# ==========================

@app.get("/connectivity")
def connectivity_status():
    """Return unified connectivity status."""

    return connectivity_api.status()


@app.get("/connectivity/health")
def connectivity_health():
    """Return connectivity health."""

    return connectivity_api.health()


@app.get("/connectivity/networks")
def connectivity_networks():
    """Return safely discoverable visible networks."""

    return connectivity_api.networks()


@app.get("/connectivity/servers")
def connectivity_servers():
    """Return configured server health information."""

    return connectivity_api.servers()


@app.get("/connectivity/satellite")
def connectivity_satellite():
    """Return satellite connectivity status."""

    return connectivity_api.satellite()


@app.post("/connectivity/satellite/ingest")
def connectivity_satellite_ingest(
    data: Dict[str, object],
):
    """Ingest approved satellite telemetry."""

    return connectivity_api.ingest_satellite(data)


@app.post("/connectivity/start")
def connectivity_start():
    """Start the connectivity engine."""

    return connectivity_api.start()


@app.post("/connectivity/stop")
def connectivity_stop():
    """Stop the connectivity engine."""

    return connectivity_api.stop()


@app.post("/connectivity/restart")
def connectivity_restart():
    """Restart the connectivity engine."""

    return connectivity_api.restart()


# ==========================
# HOME
# ==========================

@app.get("/")
def home():
    """Return MAIN BASE FOUNDATION API status."""

    return {
        "project": "MAIN BASE FOUNDATION",
        "version": "1.0.0",
        "status": "RUNNING",
    }
