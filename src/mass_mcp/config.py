"""Configuration for the Music Assistant MCP Server."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Server settings loaded from environment variables."""

    mass_url: str = "http://localhost:8095"
    mass_token: str = ""

    # Server transport settings
    host: str = "0.0.0.0"
    port: int = 8086

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
