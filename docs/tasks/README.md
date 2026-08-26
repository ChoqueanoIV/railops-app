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

As entregas 020–026 ainda são propostas condicionadas às decisões de negócio
registradas no roadmap. Criar a task detalhada somente após aprovar seu gate.

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
