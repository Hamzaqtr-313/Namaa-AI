# Namaa

A privacy-first, bilingual (Arabic/English) AI operations copilot for SMEs. See
`Namaa — Architecture Blueprint & Implementation Plan.pdf` for the full architecture
and 36-week phased roadmap. This repo implements that plan phase by phase.

## Status

**Phase 0: Foundation** — in progress. See `docs/architecture/phase-0.md`.

## Quickstart (dev)

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
docker compose up --build
```

- API: http://localhost:8000/api/docs
- Frontend: http://localhost:3000
- MinIO console: http://localhost:9001 (minio / minio123)
- Grafana: http://localhost:3001

## Repository layout

```
backend/        FastAPI + Celery + SQLAlchemy (async) application
frontend/       Next.js 14 App Router dashboard (Arabic/English, RTL/LTR)
infrastructure/ Prometheus config, Kubernetes manifests (added in Phase 6)
docs/           Architecture decision records, runbooks, phase notes
```

## Running tests

```bash
cd backend
pip install -e ".[dev]"
pytest
```

Requires a Postgres + Redis instance reachable at the URLs in `.env` — the
easiest way is `docker compose up db redis -d` first.
