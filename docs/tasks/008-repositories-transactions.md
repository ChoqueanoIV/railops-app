# Repositories e fronteira transacional

Status: `TODO`

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
- [ ] sessão não é criada por operação de repository;
- [ ] responsabilidades de commit são documentadas;
- [ ] queries relevantes estão encapsuladas;
- [ ] erros de persistência não vazam cruamente ao HTTP;
- [ ] integração com PostgreSQL/Alembic permanece.

## Evidências

Preencher ao executar a task:

- Branch:
- Commits:
- Testes antes:
- Testes depois:
- Lint:
- Type-check:
- Observações:
