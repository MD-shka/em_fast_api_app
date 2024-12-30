"""Create config for testing"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="/home/em_fast_api_app/.env.test", env_file_encoding="utf-8")

    TEST_POSTGRES_USER: object = model_config.get("TEST_POSTGRES_USER")
    TEST_POSTGRES_PASSWORD: object = model_config.get("TEST_POSTGRES_PASSWORD")
    TEST_POSTGRES_DB: object = model_config.get("TEST_POSTGRES_DB")
    TEST_POSTGRES_HOST: object = model_config.get("TEST_POSTGRES_HOST")
    TEST_POSTGRES_PORT: object = model_config.get("TEST_POSTGRES_PORT")
    TEST_REDIS_PORT: object = model_config.get("TEST_REDIS_PORT")
    TEST_REDIS_HOST: object = model_config.get("TEST_REDIS_HOST")
    TEST_REDIS_DB: object = model_config.get("TEST_REDIS_DB")

    @property
    def get_db_url(self) -> str:
        """Get database URL."""
        return f"postgresql+asyncpg://{self.TEST_POSTGRES_USER}:{self.TEST_POSTGRES_PASSWORD}@{self.TEST_POSTGRES_HOST}:{self.TEST_POSTGRES_PORT}/{self.TEST_POSTGRES_DB}"

    @property
    def get_redis_url(self) -> str:
        """Get redis URL."""
        return f"redis://{self.TEST_REDIS_HOST}:{self.TEST_REDIS_PORT}/{self.TEST_REDIS_DB}"


test_settings: Settings = Settings()
