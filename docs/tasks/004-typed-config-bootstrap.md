# Configuração tipada e bootstrap da aplicação

Status: `TODO`

## Objetivo
Centralizar configuração e inicialização do FastAPI.

## Escopo
- criar configuração tipada;
- centralizar variáveis de ambiente;
- revisar criação de engine/session;
- mover bootstrap para `backend/app/main.py` se adequado;
- manter entrypoint compatível temporariamente quando necessário;
- preparar configuração por ambiente sem secrets versionados.

## Critérios de aceite
- [ ] configuração possui tipos;
- [ ] app inicia com configuração válida;
- [ ] erro de variável obrigatória é claro;
- [ ] testes não dependem de credenciais reais;
- [ ] Swagger continua acessível.

## Evidências

Preencher ao executar a task:

- Branch:
- Commits:
- Testes antes:
- Testes depois:
- Lint:
- Type-check:
- Observações:
