# Estado atual observado

Baseado no repositório público `ChoqueanoIV/railops-app` consultado em 15/08/2026.

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
    models/
    repositories/
    routers/
    schemas/
    services/
  tests/
  alembic.ini
  main.py
  requirements.txt
```

A base já possui separação por camadas. O trabalho proposto é amadurecer contratos e organização, não reconstruir do zero.

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

O README público informa uma suíte de 48 testes no estado consultado.

## Frontend

O README descreve o frontend atual como HTML, CSS e JavaScript.

A modernização para React + TypeScript deve ser tratada como migração incremental, não substituição imediata.

## Dependências

O backend usa `requirements.txt` fixado por versão.

A maturidade desejada inclui:
- manifesto de projeto;
- separação runtime/dev;
- lockfile;
- lint;
- formatter;
- type-check;
- coverage;
- automação.
