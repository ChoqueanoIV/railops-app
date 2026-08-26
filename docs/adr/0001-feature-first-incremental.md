# 0001 — Arquitetura feature-first incremental

Status: Aceito

## Contexto

O backend começou organizado por camadas globais. Uma migração completa de uma
vez elevaria o risco de regressão nas regras ferroviárias e dificultaria revisão
e rollback.

## Decisão

Organizar código novo por feature e migrar o existente incrementalmente. Cada
feature reúne controller, schemas, service, repository, modelos e exceções. A
direção de dependências é controller → service → repository/persistência.
Adaptadores nos pacotes antigos permanecem somente enquanto houver consumidores.

## Alternativas consideradas

- manter apenas camadas globais;
- reescrever todo o backend em uma migração big bang;
- criar abstrações completas para uma arquitetura alvo antes de haver uso real.

## Consequências

Auth e passagens podem evoluir isoladamente e cada migração cabe em um PR
reversível. Durante a transição existe duplicidade aparente de caminhos e os
adaptadores precisam de remoção explícita quando deixarem de ser necessários.
