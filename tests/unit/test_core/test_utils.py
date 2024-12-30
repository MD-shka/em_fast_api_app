"""Test case for get_expiration_time function."""

from datetime import datetime

import pytest

import app.core.utils as utils_module


@pytest.fixture(autouse=True)
def reset_expiration_time():
    """Сбрасывает _next_expiration_time перед каждым тестом."""
    original_value = utils_module._next_expiration_time
    utils_module._next_expiration_time = None
    yield
    utils_module._next_expiration_time = original_value


@pytest.fixture
def mock_datetime(monkeypatch):
    """Fixture for datetime.now."""

    class MockDatetime:
        """Mock datetime.now class."""

        mocked_now = None

        @classmethod
        def now(cls):
            """Return mocked_now."""
            return cls.mocked_now

    def set_now(dt):
        """Set mocked_now to dt."""
        MockDatetime.mocked_now = dt

    monkeypatch.setattr("app.core.utils.datetime", MockDatetime)
    return set_now


def test_get_expiration_time_before_refresh(mock_datetime):
    mock_datetime(datetime(2023, 1, 1, 10))
    expiration_time = utils_module.get_expiration_time()
    expected_time = datetime(
        2023, 1, 1, utils_module.CACHE_REFRESH_HOUR, utils_module.CACHE_REFRESH_MINUTE
    ).timestamp()
    assert expiration_time == int(expected_time)


def test_get_expiration_time_after_refresh(mock_datetime):
    mock_datetime(datetime(2023, 1, 1, 15))
    expiration_time = utils_module.get_expiration_time()
    expected_time = datetime(
        2023, 1, 2, utils_module.CACHE_REFRESH_HOUR, utils_module.CACHE_REFRESH_MINUTE
    ).timestamp()
    assert expiration_time == int(expected_time)
