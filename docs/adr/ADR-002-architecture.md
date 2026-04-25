# ADR 002 — Arquitetura interna (padrão de pastas)

Decisão: organizar a aplicação seguindo uma separação clara entre camadas:

- `domain/` — entidades e regras de negócio.
- `application/` — casos de uso (service layer, orquestração).
- `infrastructure/` — integrações externas (DB, redis, gateways).
- `presentation/` — rotas HTTP, templates, validação de entradas.

No template a estrutura física proposta é:

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

Motivação: separação de responsabilidades, facilidade de testes e menor acoplamento.
