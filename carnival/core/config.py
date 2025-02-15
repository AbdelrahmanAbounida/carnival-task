import os
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    PORT: int = os.environ.get("PORT", 7000)
    HOST: str = os.environ.get("HOST", "0.0.0.0")
    CURRENT_VERSION: str = "v1"
    SERVER_API_KEY: str = os.environ.get("SERVER_API_KEY", "")

    ROUTE_SERVICE_BASE_FILE: str = "resources"  # TODO:: this should be basic api route
    OPTIMIZATION_SERVICE_BASE_FILE: str = "resources"

    # running environment
    ENV: Literal["online", "local"] = os.environ.get("ENVIRONMENT", "local")

    model_config = SettingsConfigDict(
        env_file="../.env", env_ignore_empty=True, extra="ignore"
    )


settings = Settings()  # type: ignore
