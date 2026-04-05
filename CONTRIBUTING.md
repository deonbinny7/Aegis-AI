# Contributing to Altair AI

Thank you for your interest in contributing to Altair AI! As an open-source project, we welcome contributions from developers, architects, technical writers, and researchers.

Please review this guide to understand our development workflow, coding standards, and release processes.

---

## 🛠️ Local Development Setup

To set up a local development environment:

### Backend Setup
1. Create a virtual environment using Python 3.11+:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the development database and migrations:
   ```bash
   alembic upgrade head
   ```
4. Run the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install packages:
   ```bash
   npm install
   ```
3. Run the Vite development server:
   ```bash
   npm run dev
   ```

---

## 🌿 Git Branching Model

1. Fork the repository and create your branch from `main`:
   ```bash
   git checkout -b feature/your-awesome-feature
   ```
2. Keep your branch updated by rebasing against `main` regularly:
   ```bash
   git pull --rebase origin main
   ```
3. Follow the commit message guidelines below.

---

## 📝 Commit Message Convention

We enforce semantic commit messages to automatically build our changelogs. Use the following format:

`type(scope): description`

### Allowed Types:
- `feat`: A new user-facing feature.
- `fix`: A bug fix.
- `docs`: Documentation changes only.
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc).
- `refactor`: A code change that neither fixes a bug nor adds a feature.
- `perf`: A code change that improves performance.
- `test`: Adding missing tests or correcting existing tests.
- `chore`: Changes to the build process or auxiliary tools/libraries.

### Example:
`feat(router): add cerebras provider with automatic fallback`

---

## 🧪 Testing Guidelines

Before submitting your PR:
1. Ensure all backend tests pass:
   ```bash
   cd backend
   pytest tests/
   ```
2. Ensure frontend code passes linting and compiles:
   ```bash
   cd frontend
   npm run lint
   npm run build
   ```

---

## 🚀 Pull Request Workflow

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-awesome-feature
   ```
2. Open a Pull Request against the `main` branch of `deonbinny7/AltairAI`.
3. Provide a clear description of the problem solved, architectural changes made, and steps taken to verify correctness.
4. One of the core maintainers will review your PR and coordinate any changes.
