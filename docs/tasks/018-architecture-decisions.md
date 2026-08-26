# ADRs e governança arquitetural

Status: `CONCLUÍDA`

## Objetivo
Registrar decisões que seriam difíceis de reconstruir no futuro.

## Criar ADR quando decidir
- arquitetura feature-first;
- envelope REST;
- gerenciador Python;
- estratégia de transações;
- abordagem de domínio/ORM;
- React/Vite;
- armazenamento de token;
- Docker/deploy.

## Formato
Criar `docs/adr/NNNN-titulo.md` com:
- contexto;
- decisão;
- alternativas;
- consequências;
- status.

## Critérios de aceite
- [x] decisões relevantes possuem rationale;
- [x] ADR não vira documentação de implementação trivial.

## Evidências

Preencher ao executar a task:

- Branch: `docs/adrs-governanca`
- Commits: preenchido após o commit da entrega.
- Testes antes: backend 133 aprovados, cobertura 94,06%; frontend 13 aprovados.
- Testes depois: backend 133 aprovados, cobertura 94,06%; frontend 13 aprovados.
- Lint: Ruff, Ruff format, pre-commit, ESLint e Prettier aprovados.
- Type-check: mypy e TypeScript aprovados; build Vite aprovado.
- Observações: criados oito ADRs aceitos para feature-first incremental,
  envelope de erro compatível, `uv`, transações, uso pragmático de ORM,
  React/Vite, token em `sessionStorage` e Docker local com decisão de deploy
  ainda aberta. O índice define numeração, estados e substituição de decisões.
  Todos os ADRs possuem contexto, decisão, alternativas e consequências; links
  internos foram validados. Nenhum código funcional foi alterado.
