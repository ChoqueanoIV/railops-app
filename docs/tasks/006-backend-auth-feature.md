# Migrar autenticação para feature

Status: `CONCLUÍDA`

## Objetivo
Usar autenticação como primeira migração arquitetural por feature.

## Escopo
Criar/organizar:
- controller;
- schemas;
- service/use cases;
- repository quando existir persistência;
- entities/types;
- exceptions;
- dependencies de auth;
- testes unit/api.

## Regras
- preservar matrícula/PIN/JWT e primeiro acesso;
- não trocar algoritmo/fluxo de autenticação sem requisito;
- não alterar claims do JWT sem necessidade explícita.

## Critérios de aceite
- [x] controller contém apenas HTTP/orquestração de borda;
- [x] regras estão no service;
- [x] banco está isolado;
- [x] testes de caracterização continuam passando;
- [x] imports antigos removidos ou adaptados de forma temporária documentada.

## Evidências

Preencher ao executar a task:

- Branch: `refactor/auth-feature`
- Commits: `893c085` (`refactor: organiza autenticacao por feature`) e
  `3e69a0d` (`docs: registra migracao da autenticacao`)
- Testes antes: `109 passed`
- Testes depois: `110 passed`; cobertura total de `94%`
- Lint: Ruff e formatter Ruff aprovados pelo pre-commit
- Type-check: `mypy` aprovado no escopo configurado
- Observações: matrícula, PIN, algoritmo HS256, claims `sub`/`matricula`,
  expiração de 480 minutos, primeiro acesso e contratos HTTP foram preservados.
  Os módulos antigos permanecem como adaptadores de reexportação temporários e
  possuem teste de identidade para impedir modelos ou contratos duplicados.
