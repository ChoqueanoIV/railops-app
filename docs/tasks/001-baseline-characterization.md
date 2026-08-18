# Baseline e testes de caracterização

Status: `CONCLUÍDA`

## Objetivo
Congelar o comportamento atual antes da refatoração arquitetural.

## Escopo
- executar suíte atual;
- registrar comandos e resultado;
- mapear endpoints;
- mapear regras críticas de auth, Brisamar e TECON;
- identificar buracos de cobertura;
- adicionar testes de caracterização necessários.

## Critérios de aceite
- [x] suíte atual executada e resultado registrado;
- [x] endpoints públicos inventariados;
- [x] principais requests/responses registrados;
- [x] regras críticas cobertas por teste observável;
- [x] nenhum comportamento de produção alterado;
- [x] documento de baseline criado em `docs/architecture/baseline.md`.

## Fora de escopo
- mover pastas;
- mudar response;
- trocar dependências;
- modernizar frontend.

## Evidências

Preencher ao executar a task:

- Branch: `test/baseline-characterization`
- Commits: `293bd27` (testes) e commit documental de conclusão desta task
- Testes antes: `88 passed` com Pytest 9.1.1 e Python 3.13.0
- Testes depois: `100 passed` com Pytest 9.1.1 e Python 3.13.0
- Lint: ainda não configurado; responsabilidade da task 002
- Type-check: ainda não configurado; responsabilidade da task 002
- Observações: foram adicionados somente testes de caracterização de login,
  rotas de autenticação e superfície OpenAPI. Nenhum arquivo de produção,
  contrato HTTP, migration, dependência ou regra de negócio foi alterado.
