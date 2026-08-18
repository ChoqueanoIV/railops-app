---
name: railops-react
description: Use na criação ou migração incremental do frontend RailOps para React + TypeScript + Vite, incluindo estrutura, componentes, rotas, API client, aliases, ESLint, Prettier e testes.
---

# React RailOps

Stack alvo:
- React + TypeScript;
- Vite;
- React Router;
- ESLint + Prettier;
- Vitest + Testing Library.

Migração:
1. criar shell;
2. manter legado funcional;
3. criar API client tipado;
4. migrar uma rota/feature por vez;
5. validar paridade;
6. remover legado somente após substituição completa.

Nunca criar `fetch` espalhado em componentes.
Preferir feature-first.
Configurar `@/` para `src/`.
