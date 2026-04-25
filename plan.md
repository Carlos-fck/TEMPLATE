A melhor forma de pensar esse template é como um “boilerplate de produção”, não um projeto de app.

Ou seja: ele precisa resolver infraestrutura, DX (developer experience), deploy, observabilidade e padrões arquiteturais — sem acoplamento ao domínio.

Vou estruturar em tarefas atômicas, em ordem de execução, para você construir isso do zero e publicar como template open source.


---

Plano de execução — Template Base Python

Fase 0 — Definição arquitetural

Objetivo: congelar decisões.


---

Tarefa 0.1 — Definir arquitetura base

Decidir:

framework web (recomendo FastAPI ou Flask)


Como você citou:

Jinja2

Celery

Alembic


Minha recomendação:

FastAPI + Jinja2

Motivos:

ASGI moderno

tipagem forte

excelente DI

bom suporte async

fácil coexistência com Jinja


Entregável:

ADR-001-framework.md


---

Tarefa 0.2 — Definir padrão arquitetural interno

Escolher padrão:

app/
├── domain/
├── application/
├── infrastructure/
├── presentation/

Separação:

Domain:

entidades

regras de negócio


Application:

use cases


Infrastructure:

banco

redis

celery


Presentation:

rotas

templates

api


Entregável:

ADR-002-architecture.md


---

Tarefa 0.3 — Definir convenções

Definir:

naming

imports

services

repositories

schemas

DTOs


Entregável:

CONVENTIONS.md


---

Fase 1 — Inicialização do repositório


---

Tarefa 1.1 — Criar repositório GitHub

Configurar:

nome

descrição

license MIT


Entregável:

repositório criado


---

Tarefa 1.2 — Criar estrutura inicial

Criar:

src/
tests/
infra/
docs/
scripts/


---

Tarefa 1.3 — Inicializar projeto uv

Criar:

uv init


---

Tarefa 1.4 — Configurar Python 3.14

Definir:

requires-python = ">=3.14"


---

Tarefa 1.5 — Configurar dependências base

Adicionar:

uv add fastapi
uv add jinja2
uv add sqlalchemy
uv add psycopg
uv add alembic
uv add celery
uv add redis
uv add pydantic-settings
uv add python-multipart
uv add uvicorn


---

Tarefa 1.6 — Configurar dependências dev

Adicionar:

uv add --dev pytest
uv add --dev pytest-asyncio
uv add --dev ruff
uv add --dev mypy
uv add --dev pre-commit


---

Fase 2 — Estrutura da aplicação


---

Tarefa 2.1 — Criar árvore de diretórios

src/app/

Subpastas:

config/
db/
models/
repositories/
services/
workers/
templates/
static/
routes/
tasks/


---

Tarefa 2.2 — Criar app factory

Implementar:

create_app()


---

Tarefa 2.3 — Configurar settings centralizados

Implementar:

BaseSettings

Separar:

dev

prod

test



---

Tarefa 2.4 — Configurar carregamento de .env

Criar:

.env.example


---

Fase 3 — Banco de dados


---

Tarefa 3.1 — Configurar engine SQLAlchemy

Criar:

engine.py
session.py
base.py


---

Tarefa 3.2 — Configurar Alembic

Inicializar:

alembic init


---

Tarefa 3.3 — Integrar metadata ao Alembic

Configurar:

target_metadata


---

Tarefa 3.4 — Criar primeira migration

Migration base


---

Tarefa 3.5 — Criar script de upgrade automático

Criar:

scripts/migrate.sh


---

Fase 4 — Redis


---

Tarefa 4.1 — Configurar cliente Redis

Criar singleton.


---

Tarefa 4.2 — Configurar cache helper

Criar abstração:

cache.get()
cache.set()


---

Tarefa 4.3 — Configurar healthcheck Redis

Criar endpoint.


---

Fase 5 — Celery


---

Tarefa 5.1 — Configurar Celery app

Criar:

celery_app.py


---

Tarefa 5.2 — Configurar broker Redis

Separar:

broker/result backend


---

Tarefa 5.3 — Criar task exemplo

Task:

ping


---

Tarefa 5.4 — Criar autodiscovery

Tasks automáticas.


---

Tarefa 5.5 — Configurar retries padrão

Retries exponenciais.


---

Fase 6 — Frontend server-side


---

Tarefa 6.1 — Configurar Jinja2

Engine templates.


---

Tarefa 6.2 — Configurar static files

CSS/JS.


---

Tarefa 6.3 — Criar layout base

Criar:

base.html


---

Tarefa 6.4 — Criar página inicial

Landing mínima.


---

Tarefa 6.5 — Criar macros reutilizáveis

Componentização.


---

Fase 7 — Docker


---

Tarefa 7.1 — Criar Dockerfile multi-stage

Objetivos:

imagem pequena

build rápido


Base recomendada:

python:3.14-slim


---

Tarefa 7.2 — Otimizar instalação uv

Cache layers.


---

Tarefa 7.3 — Criar docker-entrypoint.sh

Responsabilidades:

migrate

iniciar app



---

Fase 8 — Docker Compose


---

Tarefa 8.1 — Criar serviço app

Container web.


---

Tarefa 8.2 — Criar serviço worker

Celery worker.


---

Tarefa 8.3 — Criar serviço redis

Redis alpine.


---

Tarefa 8.4 — Criar serviço postgres

Postgres 17 alpine.


---

Tarefa 8.5 — Configurar volumes

Persistência.


---

Tarefa 8.6 — Configurar network

Rede interna.


---

Tarefa 8.7 — Configurar healthchecks

Todos os serviços.


---

Tarefa 8.8 — Configurar restart policy

unless-stopped


---

Fase 9 — Coolify


---

Tarefa 9.1 — Adaptar compose para Coolify

Compatibilidade.


---

Tarefa 9.2 — Configurar variáveis

Secrets.


---

Tarefa 9.3 — Configurar domínio

Proxy reverso.


---

Tarefa 9.4 — Configurar health endpoint

/health


---

Fase 10 — Observabilidade


---

Tarefa 10.1 — Configurar logging estruturado

JSON logs.


---

Tarefa 10.2 — Criar correlation id middleware

Tracing.


---

Tarefa 10.3 — Criar endpoint readiness

/ready


---

Tarefa 10.4 — Criar endpoint liveness

/live


---

Fase 11 — Qualidade


---

Tarefa 11.1 — Configurar Ruff

Lint.


---

Tarefa 11.2 — Configurar MyPy

Tipagem.


---

Tarefa 11.3 — Configurar Pytest

Tests.


---

Tarefa 11.4 — Criar testes de smoke

Web, DB, Redis.


---

Tarefa 11.5 — Configurar pre-commit

Hooks.


---

Fase 12 — Automação


---

Tarefa 12.1 — Criar Makefile

Comandos:

dev
test
lint
format
migrate
worker
up
down


---

Tarefa 12.2 — Criar scripts utilitários

Scripts:

reset-db
seed
migrate


---

Fase 13 — CI/CD


---

Tarefa 13.1 — Configurar GitHub Actions

Pipeline.


---

Tarefa 13.2 — Rodar lint


---

Tarefa 13.3 — Rodar testes


---

Tarefa 13.4 — Build Docker


---

Fase 14 — Documentação


---

Tarefa 14.1 — README principal

Explicar:

stack

instalação

deploy



---

Tarefa 14.2 — Documentar arquitetura


---

Tarefa 14.3 — Documentar convenções


---

Tarefa 14.4 — Documentar deploy Coolify


---

Fase 15 — Template final


---

Tarefa 15.1 — Criar branch clean-template

Sem código de exemplo.


---

Tarefa 15.2 — Criar tag v1.0.0


---

Tarefa 15.3 — Marcar como GitHub Template Repository


---

Estrutura final esperada

.
├── src/
│   └── app/
├── tests/
├── alembic/
├── infra/
│   ├── docker/
│   └── compose/
├── scripts/
├── docs/
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── uv.lock
├── .env.example
├── .pre-commit-config.yaml
├── README.md

Ordem recomendada de execução

Faça exatamente nesta ordem:

Fase 0
Fase 1
Fase 2
Fase 3
Fase 4
Fase 5
Fase 6
Fase 7
Fase 8
Fase 11
Fase 12
Fase 10
Fase 13
Fase 14
Fase 15

Minha recomendação extra:

padronize isso já no template:

service layer

repository layer

unit of work

dependency injection

task orchestration

event hooks

typed settings

typed repositories

