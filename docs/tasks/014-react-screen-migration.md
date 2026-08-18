# Migração incremental das telas

Status: `TODO`

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
- [ ] nenhuma remoção prematura;
- [ ] regras continuam no backend quando são de domínio;
- [ ] formulário tipado;
- [ ] estados de loading/error/success tratados.

## Evidências

Preencher ao executar a task:

- Branch:
- Commits:
- Testes antes:
- Testes depois:
- Lint:
- Type-check:
- Observações:
