# Estado atual observado

Atualizado a partir da branch `refactor/auth-feature` em 19/08/2026.

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
    features/
      auth/
        controller.py
        dependencies.py
        exceptions.py
        models.py
        repository.py
        schemas.py
        service.py
        types.py
      passagens/
        controller.py
        exceptions.py
        models.py
        repository.py
        schemas.py
        service.py
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
compatível. Autenticação e passagens estão organizadas por feature. Os módulos
antigos em `models`, `repositories`, `routers`, `schemas` e `services` são
adaptadores temporários que reexportam os símbolos canônicos de `app.features`;
código de produção novo deve usar as features diretamente.

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

A suíte atual contém 111 testes e não depende das credenciais do `.env` real.

## Frontend

O README descreve o frontend atual como HTML, CSS e JavaScript.

A modernização para React + TypeScript deve ser tratada como migração incremental, não substituição imediata.

## Dependências

O backend usa `pyproject.toml` como manifesto, grupos separados para runtime,
testes e desenvolvimento, e `uv.lock` versionado. Os arquivos requirements são
exports compatíveis gerados a partir do mesmo lockfile.

A base de qualidade inclui Ruff, formatter do Ruff, mypy, pytest-cov e
pre-commit. A automação remota de CI ainda é uma etapa futura.
