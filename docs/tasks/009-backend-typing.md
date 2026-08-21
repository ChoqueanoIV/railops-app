# Tipagem progressiva do backend

Status: `CONCLUÍDA`

## Objetivo
Aumentar confiabilidade por type hints sem uma reescrita total.

## Escopo
- tipar funções públicas;
- tipar retornos de repositories/services;
- reduzir `Any`;
- criar aliases/types úteis;
- configurar mypy por módulos;
- tratar Optional corretamente.

## Critérios de aceite
- [x] módulos migrados passam no mypy;
- [x] nenhum `ignore` amplo;
- [x] contratos entre camadas são claros;
- [x] type hints não alteram comportamento.

## Evidências

Preencher ao executar a task:

- Branch: `refactor/backend-typing`
- Commits: `e91109b` (`refactor: fortalece tipagem do backend`)
- Testes antes: `115 passed`
- Testes depois: `116 passed`; cobertura total de `94%`
- Lint: Ruff e formatter Ruff aprovados pelo pre-commit
- Type-check: `mypy` aprovado em 45 arquivos, com `disallow_untyped_defs = true`
  e sem overrides por módulo
- Observações: controllers, validators, snapshots e métodos internos de
  passagens receberam contratos concretos. A montagem da consulta agora usa
  schemas tipados para equipe, linhas, rádios e detalhes Brisamar/TECON. Nenhum
  `Any`, cast ou `type: ignore` foi introduzido e os contratos HTTP permaneceram.
