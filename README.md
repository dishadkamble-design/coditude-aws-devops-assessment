# Coditude AWS DevOps Assessment — Step 1 Demo

This is a minimal Next.js frontend, FastAPI backend, and PostgreSQL sample application for demonstrating deployment automation. It is **not** a complete production-grade AWS implementation. The PostgreSQL password `app` is for local development only.

## Prerequisites
Docker Desktop with Docker Compose.

## Run locally
```bash
docker compose up --build -d
docker compose ps
docker compose logs --tail=50 backend
```

- Frontend: http://localhost:3000
- Backend health: http://localhost:8000/health
- API docs: http://localhost:8000/docs
- Tasks API: http://localhost:8000/api/tasks

Use the frontend to add a task and verify it appears. Stop with `docker compose down` (do not add `-v` unless you want to delete local database data).

## Architecture notes
Browser calls the backend at `NEXT_PUBLIC_API_URL`; the backend connects to PostgreSQL using `DATABASE_URL`. For AWS, replace localhost URLs with HTTPS endpoints, configure restricted CORS, and inject database credentials via AWS Secrets Manager. Production infrastructure, CloudFormation, independent CI/CD workflows, monitoring, HA, and rollback are future steps, not included here.
