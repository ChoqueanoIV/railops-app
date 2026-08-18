# Arquitetura alvo

## Princípios

- feature-first onde traz clareza;
- separação clara de responsabilidades;
- dependência sempre apontando para dentro;
- regra de negócio independente de HTTP;
- persistência encapsulada;
- contratos tipados;
- testes por nível;
- migrations versionadas;
- observabilidade e configuração centralizadas.

## Backend alvo

```text
backend/
  app/
    main.py
    api/
      router.py
      dependencies/
      errors/
        handlers.py
        schemas.py
      responses/
        schemas.py
    core/
      config.py
      database.py
      logging.py
      security.py
    features/
      auth/
        controller.py
        schemas.py
        service.py
        repository.py
        models.py
        entities.py
        exceptions.py
      passagens/
        controller.py
        schemas.py
        service.py
        repository.py
        models.py
        entities.py
        exceptions.py
      tecon/
        controller.py
        schemas.py
        service.py
        repository.py
        models.py
        entities.py
        exceptions.py
    shared/
      domain/
      persistence/
      types/
      utils/
  alembic/
  tests/
    unit/
    integration/
    api/
    fixtures/
  pyproject.toml
```

Não é obrigatório criar todos os arquivos. Só criar abstrações quando existir responsabilidade real.

## Fluxo

```text
HTTP
  ↓
Controller
  ↓
Schema de entrada
  ↓
Service / Use Case
  ↓
Domain
  ↓
Repository
  ↓
SQLAlchemy ORM
  ↓
PostgreSQL
```

Na volta:

```text
ORM/Domain
  ↓
Service result
  ↓
Response schema
  ↓
HTTP
```

## Frontend alvo

```text
frontend/
  src/
    app/
      App.tsx
      providers.tsx
    components/
    features/
      auth/
      passagens/
      tecon/
    routes/
    services/
      api/
    hooks/
    lib/
    styles/
    types/
  tests/
  index.html
  package.json
  tsconfig.json
  vite.config.ts
  eslint.config.js
  .prettierrc
```
