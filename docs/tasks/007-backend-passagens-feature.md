# Migrar passagens para features

Status: `TODO`

## Objetivo
Migrar Brisamar/TECON de forma incremental após validar o padrão com auth.

## Escopo
- mapear o que é comum e o que é específico;
- não criar herança/abstração comum prematura;
- migrar uma feature de cada vez;
- separar schemas, services, repositories, models/entities;
- preservar validações existentes.

## Critérios de aceite
- [ ] cada fluxo mantém comportamento;
- [ ] dependências entre Brisamar/TECON são explícitas;
- [ ] regra não reside em controller;
- [ ] persistência não reside em service quando pode ser repository;
- [ ] testes passam.

## Evidências

Preencher ao executar a task:

- Branch:
- Commits:
- Testes antes:
- Testes depois:
- Lint:
- Type-check:
- Observações:
