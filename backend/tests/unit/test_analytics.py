import pytest
from app.analytics.cost_engine import CostEngine
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_calculate_cost():
    # Mocking db session and provider pricing model
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_pricing = MagicMock()
    
    mock_pricing.input_price_per_token = 0.01
    mock_pricing.output_price_per_token = 0.02
    
    mock_result.scalar_one_or_none.return_value = mock_pricing
    mock_db.execute.return_value = mock_result

    cost = await CostEngine.calculate_cost(mock_db, "openai", "gpt-4o", 1000, 1000)
    assert cost == 0.03  # 1000 * 0.01 / 1000 + 1000 * 0.02 / 1000

@pytest.mark.asyncio
async def test_calculate_cost_fallback():
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result

    cost = await CostEngine.calculate_cost(mock_db, "unknown", "unknown", 1000, 1000)
    assert cost == 0.0

# Refactored for performance polish — 2026-05-31T17:37:02
