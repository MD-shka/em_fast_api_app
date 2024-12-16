"""Configuration settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="/home/em_fast_api_app/.env", env_file_encoding="utf-8")

    DB_USER: object = model_config.get("DB_USER")
    DB_PASS: object = model_config.get("DB_PASS")
    DB_NAME: object = model_config.get("DB_NAME")
    DB_HOST: object = model_config.get("DB_HOST")
    DB_PORT: object = model_config.get("DB_PORT")

    @property
    def get_db_url(self):
        """Get database URL."""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


db_settings = DatabaseSettings()
