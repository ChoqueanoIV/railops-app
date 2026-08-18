# Estado atual observado

Atualizado a partir da `main` local em 18/08/2026.

## Backend

Stack atual documentada:
- Python;
- FastAPI;
- Pydantic;
- PostgreSQL;
- SQLAlchemy;
- Alembic;
- JWT;
- Passlib/bcrypt;
- Pytest.

Estrutura atual:

```text
backend/
  alembic/
  app/
    core/
      config.py
      database.py
    main.py
    models/
    repositories/
    routers/
    schemas/
    services/
  tests/
  alembic.ini
  .env.example
  main.py
  requirements.txt
  requirements-dev.txt
```

A aplicação possui configuração tipada centralizada e fábrica de bootstrap em
`app/main.py`. O `main.py` da raiz do backend permanece como entrypoint
compatível. A base já possui separação por camadas; o trabalho proposto é
amadurecer contratos e organização, não reconstruir do zero.

## Testes existentes

O repositório já contém testes de:
- auth service;
- passagem repository;
- passagem router;
- passagem schema;
- passagem service;
- TECON model;
- TECON schema;
- TECON service.

A suíte atual contém 105 testes e não depende das credenciais do `.env` real.

## Frontend

O README descreve o frontend atual como HTML, CSS e JavaScript.

A modernização para React + TypeScript deve ser tratada como migração incremental, não substituição imediata.

## Dependências

O backend usa `pyproject.toml` como manifesto, grupos separados para runtime,
testes e desenvolvimento, e `uv.lock` versionado. Os arquivos requirements são
exports compatíveis gerados a partir do mesmo lockfile.

A base de qualidade inclui Ruff, formatter do Ruff, mypy, pytest-cov e
pre-commit. A automação remota de CI ainda é uma etapa futura.
