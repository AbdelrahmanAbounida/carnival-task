import os
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    PORT: int = os.environ.get("PORT", 7000)
    HOST: str = os.environ.get("HOST", "0.0.0.0")

    # current version
    CURRENT_VERSION: str = "v1"

    # static api key to handle our api
    SERVER_API_KEY: str = os.environ.get(
        "SERVER_API_KEY", ""
    )  # TOOD:: to be used in auth service

    # running environment
    ENV: Literal["online", "local"] = os.environ.get("ENVIRONMENT", "local")

    model_config = SettingsConfigDict(
        env_file="../.env", env_ignore_empty=True, extra="ignore"
    )


settings = Settings()  # type: ignore
