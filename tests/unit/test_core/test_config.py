"""Write a pytest test case to validate the settings loading from environment variables."""

import os
from typing import Generator

import pytest

from app.core.config import Settings


@pytest.fixture
def env_vars() -> Generator[None, None, None]:
    """Fixture to set environment variables for testing."""
    os.environ["DB_USER"] = "test_user"
    os.environ["DB_PASS"] = "test_pass"
    os.environ["DB_NAME"] = "test_db"
    os.environ["DB_HOST"] = "test_host"
    os.environ["DB_PORT"] = "5432"
    os.environ["REDIS_PORT"] = "6379"
    os.environ["REDIS_HOST"] = "redis_host"
    yield
    for key in ["DB_USER", "DB_PASS", "DB_NAME", "DB_HOST", "DB_PORT", "REDIS_PORT", "REDIS_HOST"]:
        os.environ.pop(key, None)


def test_settings_load(env_vars: None) -> None:
    settings = Settings()

    assert settings.DB_USER == "test_user"
    assert settings.DB_PASS == "test_pass"
    assert settings.DB_NAME == "test_db"
    assert settings.DB_HOST == "test_host"
    assert settings.DB_PORT == "5432"
    assert settings.REDIS_PORT == "6379"
    assert settings.REDIS_HOST == "redis_host"


def test_db_url(env_vars: None) -> None:
    settings = Settings()
    expected_url = "postgresql+asyncpg://test_user:test_pass@test_host:5432/test_db"
    assert settings.get_db_url == expected_url


def test_redis_url(env_vars: None) -> None:
    settings = Settings()
    expected_url = "redis://redis_host:6379"
    assert settings.get_redis_url == expected_url
