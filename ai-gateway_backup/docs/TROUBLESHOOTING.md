# Troubleshooting Guide — Altair AI

This guide helps resolve common issues encountered while setting up and running Altair AI.

---

## 💾 Database Issues

### Alembic Migration Mismatches
* **Symptom**: `sqlalchemy.exc.ProgrammingError` or database column missing errors.
* **Solution**: Your database schema is out of sync with migrations. Run:
  ```bash
  cd backend
  alembic upgrade head
  ```
  If in a development environment and schema conflicts remain, wipe the DB volume and restart:
  ```bash
  docker compose down -v
  docker compose up --build
  ```

---

## 🧠 Redis and Memory Issues

### Redis Connection Timeouts
* **Symptom**: `redis.exceptions.ConnectionError: Error connecting to localhost:6379`.
* **Solution**: Check that the Redis server is active:
  ```bash
  docker compose ps db_redis
  ```
  If running bare-metal, ensure the `REDIS_URL` in `.env` points to the correct host and port.

---

## 👷 Celery Worker Issues

### Worker Offline or Tasks Stuck
* **Symptom**: Request auditing logs are not populating and costs are not updated.
* **Solution**: Celery tasks are managed through Redis queues. Check that the workers are running:
  ```bash
  docker compose logs celery_worker
  ```
  Verify that the Redis service is online, as Celery relies on it as a message broker.
