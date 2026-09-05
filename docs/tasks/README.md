# Backlog de evolução técnica

Executar na ordem sugerida, salvo dependência explícita diferente.

| ID | Task | Dependência |
|---|---|---|
| 001 | Baseline e testes de caracterização | - |
| 002 | Tooling Python e pyproject | 001 |
| 003 | Dependências reproduzíveis | 002 |
| 004 | Configuração tipada e bootstrap | 002 |
| 005 | Contrato de erros e responses | 001, 004 |
| 006 | Arquitetura de autenticação por feature | 001-005 |
| 007 | Arquitetura de passagens por feature | 006 |
| 008 | Repositories e fronteira transacional | 006 |
| 009 | Tipagem progressiva do backend | 002, 006-008 |
| 010 | Testes reorganizados e cobertura | 006-009 |
| 011 | Docker e ambiente local | 003-010 |
| 012 | Shell React + TypeScript | 005 |
| 013 | Cliente API e autenticação no React | 012 |
| 014 | Migração incremental das telas | 013 |
| 015 | CI de qualidade | 002, 010, 012 |
| 016 | README e documentação final | 011-015 |
| 017 | Observabilidade, segurança e hardening | 010, 011 |
| 018 | ADRs e governança arquitetural | contínua |

As tasks 001–018 formam o pacote técnico concluído. A segunda fase está
descrita no [`roadmap do produto`](../ROADMAP.md).

| ID | Task | Dependência |
|---|---|---|
| 019 | Homologação operacional e de UX | 001–018 |
| 019A | Serialização dos erros de validação | achado da 019 |
| 019B | Ocupação completa das linhas 22 e 24 do Brisamar | achado da 019 |
| 019C | Rascunho e confirmação consolidada da passagem | 019B |
| 020 | Descoberta e contrato de consulta | 019C |
| 021 | Listagem e filtros de passagens | 020 |
| 022 | Histórico auditável de edições | 020, 021 |
| 023 | Exportações e relatórios | 021, 022 |
| 024 | Testes E2E dos fluxos críticos | 019–023 |
| 025 | Estratégia e piloto de deploy | 019, 024 |
| 026 | Remoção segura do frontend legado | 019, 024, 025 |

As correções 019B e 019C e as Tasks 020–023 estão concluídas e integradas. A
Task 024 está concluída e integrada à `main` pelo PR #47, com evidências em
[`024-e2e-critical-flows.md`](024-e2e-critical-flows.md). A Task 025 foi
concluída e integrada pelo PR #48 após aprovação explícita de seu gate em
03/09/2026. O gate da Task 026 foi aprovado em 05/09/2026 e sua execução está
pausada antes da baseline de testes.

## Como pedir uma task ao Codex

Exemplo:

```text
Leia AGENTS.md e docs/tasks/006-backend-auth-feature.md.
Execute somente essa task.
Antes de alterar código, rode a suíte relevante e descreva o comportamento atual.
Não altere regra de negócio nem contrato público fora dos critérios.
Ao terminar, rode os checks e atualize a seção Evidências da task.
```

Não peça várias tasks estruturais grandes no mesmo prompt.
