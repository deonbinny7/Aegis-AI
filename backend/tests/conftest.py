import pytest
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator

from app.main import app

@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
@pytest.fixture
def db_session():
    # Mock database session
    yield

@pytest.fixture
def redis_client():
    # Mock Redis client
    yield

@pytest.fixture
def authenticated_user():
    return {"id": 1, "username": "testuser"}

@pytest.fixture
def jwt_token():
    return "mock.jwt.token"
