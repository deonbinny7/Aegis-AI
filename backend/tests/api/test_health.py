import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_readiness_check(async_client: AsyncClient):
    response = await async_client.get("/api/v1/health/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"

@pytest.mark.asyncio
async def test_liveness_check(async_client: AsyncClient):
    response = await async_client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"
