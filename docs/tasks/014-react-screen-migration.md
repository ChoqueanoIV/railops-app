# Migração incremental das telas

Status: `CONCLUÍDA`

## Objetivo
Substituir HTML/JS legado por React por fluxo, preservando paridade.

## Ordem sugerida
1. seleção/entrada após auth;
2. Brisamar;
3. TECON;
4. histórico/edição quando implementados.

## Para cada tela
- documentar comportamento atual;
- criar equivalente React;
- conectar ao API client;
- testar;
- validar paridade;
- remover legado apenas daquela tela após validação.

## Critérios de aceite
- [x] nenhuma remoção prematura;
- [x] regras continuam no backend quando são de domínio;
- [x] formulário tipado;
- [x] estados de loading/error/success tratados.

## Evidências

Preencher ao executar a task:

- Branch: `feat/migra-telas-react`
- Commits: `1a5c0bf` (`feat: migra passagens operacionais para React`) e o
  commit documental desta evidência
- Testes antes: backend com `120 passed`; React com `10 passed`
- Testes depois: React com `13 passed`; backend com `120 passed`
- Lint: ESLint e Ruff aprovados
- Type-check: TypeScript e mypy aprovados
- Build: Vite aprovado
- Formatação: Prettier e formatter Ruff aprovados
- Observações: seleção de terminal, formulários tipados de Brisamar e
  TECON, criação, consulta para edição e confirmação foram migrados para
  rotas React protegidas. Os payloads e campos imutáveis preservam os contratos
  existentes; validações de domínio continuam no backend. Nenhum arquivo do
  backend ou do frontend legado foi removido ou alterado. A aplicação local
  respondeu no navegador e o redirecionamento sem sessão foi validado.
