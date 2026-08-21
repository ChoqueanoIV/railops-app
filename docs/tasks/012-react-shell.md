# Criar shell React + TypeScript

Status: `CONCLUÍDA`

## Objetivo
Criar a base moderna do frontend sem migrar os fluxos existentes ainda.

## Escopo
- React;
- TypeScript;
- Vite;
- React Router;
- ESLint;
- Prettier;
- Vitest;
- Testing Library;
- alias `@/`;
- estrutura feature-first;
- `.env.example`;
- scripts de qualidade.

## Critérios de aceite
- [x] `npm run dev` funciona;
- [x] `npm run build` funciona;
- [x] `npm run lint` funciona;
- [x] `npm run typecheck` funciona;
- [x] `npm test` funciona;
- [x] frontend legado ainda pode ser executado durante transição.

## Evidências

Preencher ao executar a task:

- Branch: `feat/shell-react-typescript`
- Commits: `03bf960` (`feat: cria shell React com TypeScript e Vite`) e `dac6b6d`
  (`docs: registra evidencias da task 012`)
- PR: [#31 — shell React + TypeScript](https://github.com/ChoqueanoIV/railops-app/pull/31)
- Testes antes: backend com `120 passed`; frontend legado sem suíte automatizada
- Testes depois: Vitest com `2 passed`; backend com `120 passed`
- Lint: ESLint aprovado
- Type-check: TypeScript aprovado com `tsc -b`
- Build: Vite aprovado; servidor de desenvolvimento respondeu HTTP 200
- Formatação: Prettier aprovado
- Observações: shell criado em `frontend/react` para manter os HTML, CSS e
  JavaScript legados executáveis e sem alterações. Nenhum fluxo, contrato HTTP
  ou regra de negócio foi migrado nesta task.
