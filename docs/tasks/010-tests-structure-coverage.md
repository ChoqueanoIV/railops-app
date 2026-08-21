# Reorganizar testes e cobertura

Status: `CONCLUÍDA`

## Objetivo
Dar escala à suíte conforme a arquitetura cresce.

## Escopo
Reorganizar gradualmente em:
- `unit`;
- `integration`;
- `api`;
- `fixtures`.

Adicionar:
- coverage;
- markers se úteis;
- fixtures de app/db;
- testes de exceptions/responses;
- testes de repository.

## Critérios de aceite
- [x] testes continuam fáceis de executar;
- [x] banco de teste não usa produção;
- [x] coverage é gerado;
- [x] fluxos críticos estão cobertos;
- [x] testes flakey não são aceitos como baseline.

## Evidências

Preencher ao executar a task:

- Branch: `test/reorganiza-suite-cobertura`
- Commits: `bdeade3` (`test: reorganiza suite e cobertura`) e `1bc3853`
  (`docs: registra reorganizacao dos testes`)
- Pull request: [#29](https://github.com/ChoqueanoIV/railops-app/pull/29)
- Testes antes: `116 passed`; cobertura total de `94%`
- Testes depois: `117 passed`; cobertura total de `94%`
- Grupos: `83 unit`, `13 integration` e `21 api`, todos executáveis por marker
- Lint: Ruff e formatter Ruff aprovados
- Type-check: `mypy backend` aprovado em 52 arquivos
- Qualidade: pre-commit aprovado
- Observações: a suíte foi transformada em pacote e separada em `unit`,
  `integration`, `api` e `fixtures`. Fixtures tipadas de aplicação e banco foram
  registradas globalmente. A URL de teste é isolada e possui teste explícito
  contra uso do banco de produção. Nenhuma linha da aplicação foi alterada.
