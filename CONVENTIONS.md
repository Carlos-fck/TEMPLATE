# Convenções do template

- **Naming:** módulos e arquivos em `snake_case`, classes em `PascalCase`.
- **Camadas:** prefixos `services`, `repositories`, `models`, `schemas`.
- **Schemas:** pydantic models com sufixo `Schema` (ex: `UserSchema`).
- **Repos:** interfaces nomeadas `*Repository` e implementações em `infrastructure`.
- **Settings:** usar `pydantic.BaseSettings` e carregar `.env`.
- **DI:** preferir injeção por factory ou passagem explícita de dependências.
