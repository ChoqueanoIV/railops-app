# Estratégia de testes

## Objetivo inicial

Aumentar confiança antes de refatorar.

## Níveis

A suíte do backend fica em `backend/tests` e cada nível é um pacote Python:

```text
backend/tests/
  api/
  fixtures/
  integration/
  unit/
  conftest.py
```

### Unit
Testa regra isolada:
- services;
- domínio;
- helpers.

### Integration
Testa:
- repository;
- SQLAlchemy;
- migrations;
- constraints importantes.

### API
Testa:
- endpoint;
- autenticação;
- payload;
- status;
- contrato de response;
- exception mapping.

### Frontend
Testa:
- componentes;
- formulários;
- serviços HTTP;
- rotas críticas.

## Caracterização

Antes de refatorar código sem cobertura suficiente, criar teste que descreva o comportamento atual, mesmo que a arquitetura atual não seja ideal.

## Coverage

O relatório de cobertura de statements e branches é gerado com:

```powershell
py -3.13 -m uv run pytest --cov=backend/app --cov-report=term-missing
```

Os grupos também podem ser executados isoladamente:

```powershell
py -3.13 -m uv run pytest -m unit
py -3.13 -m uv run pytest -m integration
py -3.13 -m uv run pytest -m api
```

Fixtures compartilhadas de aplicação e banco pertencem a `tests/fixtures` e
são registradas pelo `conftest.py` da raiz. A configuração de teste deve usar
`RAILOPS_ENV=test` e banco cujo nome seja explicitamente `railops_test`.

Não transformar percentual em objetivo cego. Cobrir primeiro:
- autenticação;
- regras de passagem;
- autorização;
- validações;
- persistência crítica.

Nenhuma falha intermitente deve ser aceita como baseline. Uma falha precisa ser
reproduzida e corrigida ou registrada como bloqueio antes de prosseguir.
