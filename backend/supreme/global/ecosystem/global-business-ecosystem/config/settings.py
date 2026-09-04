"""
Global Business Ecosystem
Runtime Configuration
"""

import os


class Settings:
    APP_NAME: str = os.getenv(
        "APP_NAME",
        "Global Business Ecosystem"
    )

    APP_VERSION: str = os.getenv(
        "APP_VERSION",
        "1.0.0"
    )

    ENVIRONMENT: str = os.getenv(
        "ENVIRONMENT",
        "development"
    )

    DEBUG: bool = os.getenv(
        "DEBUG",
        "false"
    ).lower() == "true"

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./global_business_ecosystem.db"
    )

    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "change-this-secret-key"
    )


settings = Settings()
