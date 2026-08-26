# CI de qualidade

Status: `CONCLUÍDA`

## Objetivo
Evitar regressões automaticamente.

## Escopo
Pipeline de PR com:
Backend:
- install;
- lint;
- type-check;
- pytest;
- coverage.

Frontend:
- install lockado;
- lint;
- typecheck;
- test;
- build.

## Critérios de aceite
- [x] CI parte de checkout limpo;
- [x] lockfiles respeitados;
- [x] falha de teste/lint bloqueia;
- [x] secrets não são necessários para testes unitários;
- [x] comandos locais e CI são equivalentes.

## Evidências

Preencher ao executar a task:

- Branch: `ci/qualidade-pr`
- Commits: `1bd6321` (`ci: automatiza qualidade de backend e frontend`) e o
  commit documental desta evidência
- PR: [#34 — CI de qualidade](https://github.com/ChoqueanoIV/railops-app/pull/34)
- Testes antes: backend com `120 passed`; React com `13 passed`
- Testes depois: backend com `123 passed`; React com `13 passed`
- Coverage: `93,70%` real, exibido como `94%` pelo relatório arredondado
- Lint: ESLint e Ruff aprovados localmente e no GitHub Actions
- Type-check: TypeScript e mypy aprovados localmente e no GitHub Actions
- Build: Vite aprovado localmente e no GitHub Actions
- Formatação: Prettier e formatter Ruff aprovados
- Observações: jobs independentes de backend e frontend passaram na primeira
  execução remota. O backend usa PostgreSQL efêmero e credenciais fictícias;
  as dependências são instaladas com `uv sync --frozen` e `npm ci`. O workflow
  possui apenas `contents: read` e não consome secrets do repositório.
