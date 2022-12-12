"""Testing conf module."""
# third-party
import pytest
from falcon import testing

from .app import app_hook, app_middleware


@pytest.fixture
def client_hook() -> testing.TestClient:
    """Create testing client fixture for hook app"""
    return testing.TestClient(app_hook)


@pytest.fixture
def client_middleware() -> testing.TestClient:
    """Create testing client fixture for middleware app"""
    return testing.TestClient(app_middleware)
