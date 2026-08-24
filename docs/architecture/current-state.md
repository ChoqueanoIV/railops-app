# Estado atual observado

Atualizado a partir da branch `feat/react-api-auth` em 23/08/2026.

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
compose.yaml
.dockerignore
.env.docker.example
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

A suíte atual contém 120 testes, mantém cobertura total de 94% e não depende
das credenciais do `.env` real. A fixture de banco exige `RAILOPS_ENV=test` e o
banco `railops_test`, reduzindo o risco de execução contra produção.

## Ambiente Docker

O backend possui imagem multi-stage baseada em Python 3.13, executada por
usuário não-root e com healthcheck em `/health`. O `compose.yaml` fornece um
PostgreSQL local opcional, aguarda a saúde do banco e executa as migrations
Alembic antes de iniciar o Uvicorn. Segredos são exigidos em tempo de execução
por `.env.docker`, que permanece ignorado; somente o exemplo é versionado.

A estrutura e os requisitos de segurança foram validados por testes. O build
da imagem, a subida real do Compose, os healthchecks, a cadeia Alembic até
`head`, o usuário não-root e Swagger HTTP 200 foram confirmados localmente com
Docker Desktop e WSL 2.

## Frontend

O shell moderno está isolado em `frontend/react`, com React, TypeScript, Vite,
React Router, ESLint, Prettier, Vitest e Testing Library. O alias `@/` aponta
para `src/`, e a estrutura inicial separa aplicação, rotas, features, estilos e
infraestrutura de testes.

O React possui cliente HTTP central tipado com base URL por ambiente, timeout,
header bearer, normalização do envelope de erro e tratamento de 401/403. Login,
primeiro acesso, sessão em `sessionStorage`, logout e proteção da rota inicial
usam os contratos existentes do backend.

As rotas React protegidas agora cobrem seleção de terminal, criação e edição
das passagens do Brisamar e TECON e a confirmação do registro. Os formulários
usam tipos alinhados aos schemas da API e o cliente HTTP central; regras de
domínio e autorização de edição permanecem no backend.

Os arquivos HTML, CSS e JavaScript anteriores permanecem intactos como fallback
temporário, permitindo validação operacional antes de sua remoção em uma etapa
posterior. Histórico, filtros e relatórios ainda não possuem telas dedicadas.

## Dependências

O backend usa `pyproject.toml` como manifesto, grupos separados para runtime,
testes e desenvolvimento, e `uv.lock` versionado. Os arquivos requirements são
exports compatíveis gerados a partir do mesmo lockfile.

A base de qualidade inclui Ruff, formatter do Ruff, mypy com assinaturas
obrigatórias e sem exceções por módulo, pytest-cov e pre-commit. A automação
remota de CI ainda é uma etapa futura.
