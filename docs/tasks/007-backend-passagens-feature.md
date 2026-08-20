# Migrar passagens para features

Status: `CONCLUÍDA`

## Objetivo
Migrar Brisamar/TECON de forma incremental após validar o padrão com auth.

## Escopo
- mapear o que é comum e o que é específico;
- não criar herança/abstração comum prematura;
- migrar uma feature de cada vez;
- separar schemas, services, repositories, models/entities;
- preservar validações existentes.

## Critérios de aceite
- [x] cada fluxo mantém comportamento;
- [x] dependências entre Brisamar/TECON são explícitas;
- [x] regra não reside em controller;
- [x] persistência não reside em service quando pode ser repository;
- [x] testes passam.

## Evidências

Preencher ao executar a task:

- Branch: `refactor/passagens-feature`
- Commits: `bade0be` (`refactor: organiza passagens por feature`)
- Testes antes: `110 passed`
- Testes depois: `111 passed`; cobertura total de `94%`
- Lint: Ruff e formatter Ruff aprovados pelo pre-commit
- Type-check: `mypy` aprovado no escopo configurado
- Observações: Brisamar e TECON permanecem explícitos em schemas e métodos do
  service, compartilhando somente o agregado, edição, histórico e persistência
  que já eram comuns. Não foi criada herança. Os módulos antigos são adaptadores
  temporários, e um teste garante que reexportam as mesmas classes, inclusive
  modelos ORM. As exceções progressivas do mypy apenas acompanharam os novos
  caminhos canônicos, sem ampliar os códigos desabilitados.
