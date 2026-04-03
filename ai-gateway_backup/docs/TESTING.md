# Testing Guide — Altair AI

This guide covers running backend and frontend test suites, mocking APIs, and validating performance metrics.

---

## 🐍 Backend Testing (pytest)

We write unit and integration tests using `pytest` and `pytest-asyncio`.

### Running tests:
1. Ensure your virtual environment is active:
   ```bash
   cd backend
   source .venv/bin/activate
   ```
2. Run the complete test suite:
   ```bash
   pytest
   ```
3. Run tests with coverage reporting:
   ```bash
   pytest --cov=app --cov-report=html
   ```

---

## 🔍 Test Categories

### 1. Unit Tests
* **Guardrails testing (`tests/unit/test_guardrails.py`)**: Asserts that phone number formats, emails, and prompt injection patterns are matched and redacted.
* **Router testing (`tests/unit/test_router.py`)**: Mocks network endpoints and validates that the routing service selects fallback models correctly when primary connections fail.

### 2. Integration Tests
* **FastAPI endpoint testing (`tests/integration/test_chat.py`)**: Uses `httpx.AsyncClient` to perform request cycles against `/api/v1/chat`, validating status codes, response shapes, and database commits.

---

## 🎭 Mocking Provider Clients

To test model execution without spending credits or hitting rate limits, mock external APIs using `unittest.mock`:

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_llm_execution():
    with patch("app.ai.providers.factory.GroqProvider.generate", new_callable=AsyncMock) as mock_generate:
        mock_generate.return_value = "Mocked completion text"
        # Trigger the chat router, validating that it accesses the mock correctly.
```
