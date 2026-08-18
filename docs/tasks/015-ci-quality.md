# CI de qualidade

Status: `TODO`

## Objetivo
Evitar regressões automaticamente.

## Escopo
Pipeline de PR com:
Backend:
- install;
- lint;
- type-check;
- pytest;
- coverage.

Frontend:
- install lockado;
- lint;
- typecheck;
- test;
- build.

## Critérios de aceite
- [ ] CI parte de checkout limpo;
- [ ] lockfiles respeitados;
- [ ] falha de teste/lint bloqueia;
- [ ] secrets não são necessários para testes unitários;
- [ ] comandos locais e CI são equivalentes.

## Evidências

Preencher ao executar a task:

- Branch:
- Commits:
- Testes antes:
- Testes depois:
- Lint:
- Type-check:
- Observações:
