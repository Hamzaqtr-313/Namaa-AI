# Phase 0: Foundation

**Goal (from the blueprint):** Stand up core infrastructure and development environment.

**Exit criteria:** A developer can create a tenant, register a user, log in, and see an
empty dashboard.

## What's implemented

- Monorepo layout (`backend/`, `frontend/`, `infrastructure/`), Docker Compose dev stack, GitHub Actions CI.
- PostgreSQL 16 + Redis + MinIO running via Compose; full schema from the blueprint
  (tenants, users, customers, conversations, messages, leads, quotations, documents,
  tasks, approvals, audit_log, integrations, webhooks, notifications, consent_records,
  catalog_items, workflow_templates, workflow_runs) applied via a single initial
  Alembic migration, with Row-Level Security enforced per tenant (`FORCE ROW LEVEL
  SECURITY` — required since the app connects as the table owner, which Postgres
  otherwise exempts from RLS).
- Auth: tenant registration (`POST /api/v1/auth/register`), login by
  `tenant_slug + email + password` (`POST /api/v1/auth/login`), JWT access/refresh
  tokens, `GET /api/v1/auth/me`.
- API skeleton: FastAPI app, OpenAPI docs at `/api/docs`, consistent success/error
  JSON envelope, health check.
- Multi-tenancy: `app.tenant_id` is set via `SET LOCAL` for the lifetime of each
  request's DB transaction (see `app/api/deps.py::get_tenant_db`), so every
  tenant-scoped query is automatically filtered by RLS.
- Frontend: Next.js App Router shell with `next-intl` (English + Arabic, LTR/RTL),
  a login page, and a dashboard page hitting `GET /api/v1/dashboard/today`.
- Celery app (`app/worker.py`) wired to Redis; no tasks yet — those land in Phase 1.

## Login model note

The blueprint's `POST /api/v1/auth/login` takes email/password only. Because `email`
is unique per-tenant (not globally), and Postgres RLS blocks any `users` query made
without a resolved `tenant_id`, login here also takes `tenant_slug` (resolved first
against the tenant-global `tenants` table, which has no RLS). This is the standard
multi-tenant SaaS pattern and doesn't change the blueprint's intent — the dashboard
should default this field for demo accounts via a link.

## Deliberately deferred to later phases

- Everything under Phase 1+ endpoints (conversations, leads, quotations, documents,
  approvals, dashboard metrics beyond `/today`, integrations, settings, catalog) —
  models and DB tables exist now, but no API routes yet.
- OTP endpoints, RBAC permission matrix beyond the `role` string, refresh-token
  revocation (currently stateless JWT).
- WhatsApp/email/LLM integrations — config placeholders only.
