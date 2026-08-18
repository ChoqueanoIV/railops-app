# Migrar autenticação para feature

Status: `TODO`

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
- [ ] controller contém apenas HTTP/orquestração de borda;
- [ ] regras estão no service;
- [ ] banco está isolado;
- [ ] testes de caracterização continuam passando;
- [ ] imports antigos removidos ou adaptados de forma temporária documentada.

## Evidências

Preencher ao executar a task:

- Branch:
- Commits:
- Testes antes:
- Testes depois:
- Lint:
- Type-check:
- Observações:
