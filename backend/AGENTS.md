# Backend — orientação específica

Estas regras complementam o `AGENTS.md` da raiz.

## Prioridades

1. preservar comportamento;
2. melhorar testes;
3. separar HTTP, negócio e persistência;
4. aumentar tipagem;
5. reduzir importações cruzadas;
6. manter OpenAPI funcional;
7. tornar cada feature substituível e fácil de entender.

## Limites de dependência

Direção desejada:

```text
controller -> service/use case -> repository -> ORM/database
                     |
                     -> domain
```

O domínio não deve depender de FastAPI.

Repository não deve depender de controller.

Service não deve importar `Request`, `Response` ou `HTTPException`.

Controller não deve montar query SQLAlchemy.

## Exceções

Criar exceções de aplicação/domínio e mapear para HTTP em uma camada central.

Exemplo conceitual:

```text
PassagemNotFound
      |
exception handler
      |
HTTP 404 + error.code
```

Evitar espalhar `HTTPException` nos services.

## Sessão de banco

A sessão deve entrar por dependency/injeção.

Repository recebe sessão/abstração; não cria engine por operação.

Commit/rollback deve ter dono claro.

## Imports

Preferir imports absolutos a partir do pacote `app`.

Nunca alterar `sys.path` em arquivo de produção para resolver imports.

## Testes

Estrutura alvo:

```text
tests/
  unit/
  integration/
  api/
  fixtures/
```

- unit: sem banco real;
- integration: SQLAlchemy/repository/migration;
- api: FastAPI/TestClient ou cliente async;
- fixtures: dados reutilizáveis.

Ao mover código, mover/ajustar testes na mesma task.
