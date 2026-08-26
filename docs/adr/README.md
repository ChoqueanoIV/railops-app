# Architecture Decision Records

Use ADR para decisões arquiteturais duradouras. ADRs aceitos descrevem a
decisão vigente; uma mudança posterior deve criar outro ADR e marcar o anterior
como substituído, sem reescrever o histórico.

## Índice

- [0001 — Arquitetura feature-first incremental](0001-feature-first-incremental.md)
- [0002 — Envelope de erro compatível](0002-envelope-erro-compativel.md)
- [0003 — uv como gerenciador Python](0003-uv-gerenciador-python.md)
- [0004 — Fronteira explícita de transações](0004-fronteira-transacoes.md)
- [0005 — Modelos ORM como representação interna](0005-modelos-orm-internos.md)
- [0006 — React, TypeScript e Vite](0006-react-typescript-vite.md)
- [0007 — Token de acesso em sessionStorage](0007-token-session-storage.md)
- [0008 — Docker local sem plataforma de deploy definida](0008-docker-local-deploy-aberto.md)

Modelo:

```markdown
# NNNN — Título

Status: Proposto | Aceito | Substituído

## Contexto

## Decisão

## Alternativas consideradas

## Consequências
```

## Governança

- numere ADRs sequencialmente e não reutilize números;
- registre apenas escolhas com alternativas e consequências duradouras;
- use `Proposto` enquanto a decisão estiver em discussão;
- use `Aceito` quando a decisão orientar o projeto;
- use `Substituído por ADR-NNNN` sem apagar o rationale original;
- mudanças triviais de implementação permanecem em tasks, commits ou padrões.
