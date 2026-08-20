# Repositories e fronteira transacional

Status: `CONCLUÍDA`

## Objetivo
Definir claramente quem acessa banco e quem controla transação.

## Escopo
- revisar repositories atuais;
- remover SQLAlchemy de controller;
- reduzir SQLAlchemy direto em service;
- definir interface/Protocol somente onde trouxer valor;
- padronizar sessão;
- definir commit/rollback;
- preparar testes de integração.

## Critérios de aceite
- [x] sessão não é criada por operação de repository;
- [x] responsabilidades de commit são documentadas;
- [x] queries relevantes estão encapsuladas;
- [x] erros de persistência não vazam cruamente ao HTTP;
- [x] integração com PostgreSQL/Alembic permanece.

## Evidências

Preencher ao executar a task:

- Branch: `refactor/repositories-transactions`
- Commits: `4f0ba70` (`refactor: centraliza fronteira transacional`) e `081a75e`
  (`docs: registra fronteira transacional`)
- Testes antes: `111 passed`
- Testes depois: `115 passed`; cobertura total de `94%`
- Lint: Ruff e formatter Ruff aprovados pelo pre-commit
- Type-check: `mypy` aprovado no escopo configurado
- Observações: controllers passaram a receber services por dependencies e não
  importam SQLAlchemy. `TransacaoSQLAlchemy` centraliza commit, rollback e
  refresh usando a sessão da requisição. Erros internos são convertidos em
  `PERSISTENCE_ERROR` com mensagem neutra. Engine, metadata e Alembic não foram
  alterados.
