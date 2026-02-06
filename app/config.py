"""Application configuration management."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    port: int = 8000
    host: str = "0.0.0.0"
    data_dir: str = "./data"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def db_path(self) -> str:
        """Get the database file path."""
        return f"{self.data_dir}/iframe_server.db"

    @property
    def projects_dir(self) -> str:
        """Get the projects storage directory."""
        return f"{self.data_dir}/projects"


# Global settings instance
settings = Settings()
