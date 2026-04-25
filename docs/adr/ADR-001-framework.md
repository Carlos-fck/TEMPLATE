# ADR 001 — Framework and major components

Decisão: utilizar **FastAPI** como framework web principal, **Jinja2** para server-side rendering, **SQLAlchemy** + **Alembic** para persistência e migrações, e **Celery** com **Redis** como broker/back-end de resultados para tarefas assíncronas.

Motivação:
- FastAPI: ASGI moderno, tipagem, desempenho e excelente experiência de desenvolvimento.
- Jinja2: integração simples para páginas server-side quando necessário.
- SQLAlchemy + Alembic: maturidade e compatibilidade com apps de produção.
- Celery + Redis: solução robusta e amplamente adotada para processamento background.

Entregável: referência no repositório para scaffolding e configuração inicial.
