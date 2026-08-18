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
from backend.api.cloud import CloudAPI
from backend.api.integrations import IntegrationsAPI
from backend.api.integration_connections import (
    IntegrationConnectionsAPI,
)


app = FastAPI(
    title="MAIN BASE FOUNDATION API",
    version="1.0.0",
)


# ==========================
# CORE APIs
# ==========================

connectivity_api = ConnectivityAPI()
cloud_api = CloudAPI()
integrations_api = IntegrationsAPI()
integration_connections_api = (
    IntegrationConnectionsAPI()
)


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
# CLOUD
# ==========================

@app.get("/cloud")
def cloud_status():
    """Return unified cloud status."""

    return cloud_api.status()


@app.get("/cloud/health")
def cloud_health():
    """Return cloud infrastructure health."""

    return cloud_api.health()


@app.get("/cloud/security")
def cloud_security():
    """Return cloud integration security."""

    return cloud_api.security()


@app.get("/cloud/providers")
def cloud_providers():
    """Return registered cloud providers."""

    return cloud_api.providers()


@app.get("/cloud/providers/{name}")
def cloud_provider(
    name: str,
):
    """Return one registered cloud provider."""

    return cloud_api.provider(name)


@app.get("/cloud/summary")
def cloud_summary():
    """Return compact cloud summary."""

    return cloud_api.summary()


@app.get("/cloud/services/{provider}")
def cloud_services(
    provider: str,
):
    """Return services registered for a provider."""

    return cloud_api.services(provider)


@app.post("/cloud/configure")
def cloud_configure(
    provider: str,
    region: str | None = None,
):
    """Register cloud provider configuration."""

    return cloud_api.configure(
        provider=provider,
        region=region,
    )


@app.post("/cloud/authorize")
def cloud_authorize(
    provider: str,
):
    """Record authorization from an approved flow."""

    return cloud_api.authorize(
        provider=provider,
    )


@app.post("/cloud/telemetry")
def cloud_telemetry(
    provider: str,
    online: bool,
    latency_ms: float | None = None,
):
    """Update provider availability telemetry."""

    return cloud_api.set_online(
        provider=provider,
        online=online,
        latency_ms=latency_ms,
    )


@app.post("/cloud/start")
def cloud_start():
    """Start cloud monitoring."""

    return cloud_api.start()


@app.post("/cloud/stop")
def cloud_stop():
    """Stop cloud monitoring."""

    return cloud_api.stop()


@app.post("/cloud/restart")
def cloud_restart():
    """Restart cloud monitoring."""

    return cloud_api.restart()


# ==========================
# GLOBAL INTEGRATIONS
# ==========================

@app.get("/integrations")
def integrations_definitions():
    """Return registered global integrations."""

    return integrations_api.definitions()


@app.get("/integrations/status")
def integrations_status():
    """Return safe integration readiness status."""

    return integrations_api.statuses()


@app.get("/integrations/health")
def integrations_health():
    """Return global integrations health."""

    return integrations_api.health()


@app.get("/integrations/{provider}/authorization")
def integration_authorization(
    provider: str,
):
    """Return authorization requirements."""

    return integrations_api.authorization_requirements(
        provider
    )


@app.get("/integrations/{provider}")
def integration_status(
    provider: str,
):
    """Return status for one integration provider."""

    return integrations_api.status(
        provider
    )


# ==========================
# INTEGRATION CONNECTIONS
# ==========================

@app.get("/integration-connections")
def integration_connections_statuses():
    """Return all provider connection states."""

    return integration_connections_api.statuses()


@app.get("/integration-connections/health")
def integration_connections_health():
    """Return provider connection health."""

    return integration_connections_api.health()


@app.get("/integration-connections/{provider}")
def integration_connection_status(
    provider: str,
):
    """Return one provider connection state."""

    return integration_connections_api.status(
        provider
    )


@app.post(
    "/integration-connections/{provider}/connect"
)
def integration_connection_connect(
    provider: str,
):
    """Connect an explicitly authorized provider."""

    return integration_connections_api.connect(
        provider
    )


@app.post(
    "/integration-connections/{provider}/disconnect"
)
def integration_connection_disconnect(
    provider: str,
):
    """Disconnect a provider."""

    return integration_connections_api.disconnect(
        provider
    )


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
