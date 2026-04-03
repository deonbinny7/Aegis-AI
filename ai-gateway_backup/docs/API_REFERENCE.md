# API Reference — Altair AI

Documentation for Altair AI's REST and Server-Sent Events (SSE) streaming API endpoints.

---

## 🔑 Authentication Endpoint

### `POST /api/v1/auth/login`
Logs in a user and returns a JSON Web Token (JWT).

#### Request (x-www-form-urlencoded):
- `username`: Account email or username
- `password`: Account password

#### Response:
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer"
}
```

---

## 💬 Chat Endpoints

### `POST /api/v1/chat`
Submit a message to run through the full LangGraph pipeline.

#### Request Headers:
- `Authorization: Bearer <JWT_TOKEN>`

#### Request Body (JSON):
```json
{
  "model": "llama3-70b-8192",
  "routing_strategy": "explicit",
  "messages": [
    {
      "role": "user",
      "content": "Hello! What models do you support?"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 1024,
  "prompt_name": "system_greeting",
  "prompt_variables": {
    "name": "Developer"
  }
}
```

#### Response (JSON):
```json
{
  "request_id": "8706d860-705b-4395-8e7c-ec5ee4c9ff38",
  "session_id": "31b25078-2cfa-4d1a-be10-6316239103e9",
  "message": "Hello! I support Groq, Gemini, OpenAI, Cerebras, and Anthropic.",
  "model": "llama3-70b-8192",
  "routing_strategy": "explicit",
  "retry_count": 0,
  "usage": {
    "prompt_tokens": 42,
    "completion_tokens": 20,
    "total_tokens": 62
  },
  "metadata": {
    "execution_duration": 0.345
  }
}
```

---

### `POST /api/v1/stream`
Start a Server-Sent Events (SSE) connection to stream completion responses.

#### Request Body:
Same as `/api/v1/chat`.

#### Response:
A stream of content chunks formatted as:
```text
data: {"event": "chunk", "text": "Hello"}
data: {"event": "chunk", "text": " there!"}
data: {"event": "done", "usage": {"prompt_tokens": 42, "completion_tokens": 20, "total_tokens": 62}}
```

---

## 📊 Analytics and Settings Endpoints

* **`GET /api/v1/analytics`**: Returns aggregate token consumption, latency trends, and cost calculations.
* **`GET /api/v1/settings`**: Returns current configurations (default routing, active API key state).
* **`POST /api/v1/settings`**: Update active variables (e.g. adjust model temperature limits, swap models).
