# Architecture Overview

The template follows a layered architecture to separate concerns and improve maintainability:

- `domain/` — domain entities and business rules.
- `application/` — use cases, service layer, orchestration.
- `infrastructure/` — DB, Redis, Celery adapters and external integrations.
- `presentation/` — HTTP routes, templates, static assets.

Project structure (key folders):

```
src/app/
├── config/
├── db/
├── models/
├── repositories/
├── services/
├── workers/
├── templates/
├── static/
├── routes/
└── tasks/
```

Read the ADRs in `docs/adr` for architectural decisions and rationale.
