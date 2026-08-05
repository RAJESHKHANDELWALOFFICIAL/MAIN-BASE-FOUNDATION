from fastapi import FastAPI

app = FastAPI(
    title="MAIN BASE FOUNDATION API",
    description="Digital Foundation Platform",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "project": "MAIN BASE FOUNDATION",
        "status": "RUNNING"
    }


@app.get("/health")
def health():
    return {
        "status": "OK"
    }
