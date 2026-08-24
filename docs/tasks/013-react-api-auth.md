# Cliente API tipado e autenticação React

Status: `CONCLUÍDA`

## Objetivo
Centralizar comunicação com backend e migrar o primeiro fluxo React.

## Escopo
- API client;
- base URL por ambiente;
- JWT;
- tratamento de 401/403;
- tipos request/response;
- login;
- primeiro acesso quando aplicável;
- proteção de rotas;
- testes.

## Critérios de aceite
- [x] componentes não espalham `fetch`;
- [x] auth funciona contra API existente;
- [x] erros são exibidos de forma controlada;
- [x] tokens não são logados;
- [x] fluxo possui testes.

## Evidências

Preencher ao executar a task:

- Branch: `feat/react-api-auth`
- Commit: `6937873` (`feat: integra autenticacao ao frontend React`)
- Testes antes: backend com `120 passed`; React com `2 passed`
- Testes depois: React com `10 passed`; backend com `120 passed`
- Lint: ESLint e Ruff aprovados
- Type-check: TypeScript e mypy aprovados
- Build: Vite aprovado
- Formatação: Prettier e formatter Ruff aprovados
- Observações: cliente HTTP central, login, primeiro acesso, JWT em
  `sessionStorage`, logout, 401/403 e rotas protegidas implementados contra os
  contratos existentes. Nenhum arquivo do backend ou do frontend legado foi
  alterado. O ajuste `endOfLine: auto` estabiliza o Prettier após checkout no
  Windows sem mudar conteúdo funcional.
