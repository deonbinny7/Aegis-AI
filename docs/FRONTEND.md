# Frontend Dashboard Guide — Altair AI

This document provides details on the React dashboard built with Vite, TypeScript, and TailwindCSS.

---

## 📂 Codebase Directory Structure

```text
frontend/
├── public/                 # Static assets (favicons, logos)
├── src/
│   ├── assets/             # Images and styles
│   ├── components/         # Reusable dashboard UI blocks
│   │   ├── MetricCard.tsx  # KPI counter showing costs/latency
│   │   ├── ModelChart.tsx  # Recharts chart showing token throughput
│   │   ├── LogsTable.tsx   # Request history table with filters
│   │   └── Shell.tsx       # Standard sidebar/navigation menu
│   ├── pages/              # View pages
│   │   ├── Dashboard.tsx   # Live overview, metrics, cost trends
│   │   ├── Playground.tsx  # Model query testing environment
│   │   ├── Prompts.tsx     # Template library editor and variable lists
│   │   └── Settings.tsx    # Provider key toggles and route strategies
│   ├── services/           # Service class interfacing with backend
│   │   └── api.ts          # Axios and SSE client implementations
│   ├── App.tsx             # Root router setup
│   └── main.tsx            # DOM mounting script
```

---

## ⚡ Key Views

### 1. Main Dashboard (`Dashboard.tsx`)
Displays aggregate performance metrics (Active costs, latency percentiles, error rates) and token distribution plots across Groq, Gemini, and OpenAI.

### 2. Live Playground (`Playground.tsx`)
Provides a chat interface enabling developers to:
- Select models (e.g. `llama3-70b-8192`, `gemini-1.5-flash`).
- Choose routing strategies (Explicit, cost-optimized, latency-based).
- Toggle streaming options (SSE chunks rendered as markdown).

### 3. Prompt Library (`Prompts.tsx`)
An editor interface for versioning prompt templates, defining default values, and previewing compiled prompts with dynamic variables.

// Code style format review — 2026-06-04T21:52:59
