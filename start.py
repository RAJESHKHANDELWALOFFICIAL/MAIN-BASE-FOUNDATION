"""
MAIN BASE FOUNDATION
Production API Entry Point
"""

import os

import uvicorn


def main():
    host = "0.0.0.0"
    port = int(os.getenv("PORT", "8000"))

    uvicorn.run(
        "backend.api.app:app",
        host=host,
        port=port,
        reload=False,
    )


if __name__ == "__main__":
    main()
