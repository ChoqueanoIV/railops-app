# Estado atual observado

Atualizado a partir da branch `test/reorganiza-suite-cobertura` em 21/08/2026.

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
        dependencies.py
        exceptions.py
        models.py
        repository.py
        schemas.py
        service.py
    shared/
      persistence/
        transactions.py
    main.py
    models/
    repositories/
    routers/
    schemas/
    services/
  tests/
    api/
    fixtures/
    integration/
    unit/
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

Os testes do backend estão organizados em pacotes `unit`, `integration`, `api`
e `fixtures`, com markers equivalentes para execução seletiva. O repositório
contém testes de:
- auth service;
- passagem repository;
- passagem router;
- passagem schema;
- passagem service;
- TECON model;
- TECON schema;
- TECON service.

A suíte atual contém 117 testes, mantém cobertura total de 94% e não depende
das credenciais do `.env` real. A fixture de banco exige `RAILOPS_ENV=test` e o
banco `railops_test`, reduzindo o risco de execução contra produção.

## Frontend

O README descreve o frontend atual como HTML, CSS e JavaScript.

A modernização para React + TypeScript deve ser tratada como migração incremental, não substituição imediata.

## Dependências

O backend usa `pyproject.toml` como manifesto, grupos separados para runtime,
testes e desenvolvimento, e `uv.lock` versionado. Os arquivos requirements são
exports compatíveis gerados a partir do mesmo lockfile.

A base de qualidade inclui Ruff, formatter do Ruff, mypy com assinaturas
obrigatórias e sem exceções por módulo, pytest-cov e pre-commit. A automação
remota de CI ainda é uma etapa futura.
