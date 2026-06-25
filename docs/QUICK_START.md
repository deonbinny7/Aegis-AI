# Quick Start Guide — Altair AI

This guide helps you test your gateway integration and start making requests to models.

---

## 🔐 1. Authenticate

By default, development environments include a seed administrator account (`admin` / `admin`).

Obtain your JWT Bearer token:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1Ni...",
  "token_type": "bearer"
}
```

---

## 🔀 2. Send a Chat Completion Request

Submit a message using the explicit routing strategy to direct it to Groq:

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "llama3-8b-8192",
       "routing_strategy": "explicit",
       "messages": [
         {"role": "user", "content": "Explain quantum computing in one sentence."}
       ]
     }'
```

---

## ⚡ 3. Stream a Completion (Server-Sent Events)

To receive responses character-by-character with low latency:

```bash
curl -N -X POST "http://localhost:8000/api/v1/stream" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "llama3-8b-8192",
       "messages": [
         {"role": "user", "content": "Write a 100-word poem about stars."}
       ]
     }'
```
*Your terminal will display incoming chunks in real-time.*
