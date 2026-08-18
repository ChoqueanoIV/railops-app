# Docker e ambiente local

Status: `TODO`

## Objetivo
Padronizar execução local e preparar deploy futuro.

## Escopo
- `backend/Dockerfile`;
- `.dockerignore`;
- compose local com PostgreSQL quando fizer sentido;
- healthcheck;
- migrations no fluxo documentado;
- variáveis via env;
- imagem não-root se viável;
- estratégia de frontend depois do React shell.

## Critérios de aceite
- [ ] backend sobe em container;
- [ ] banco local opcional sobe via compose;
- [ ] migration executa;
- [ ] Swagger responde;
- [ ] testes não dependem do container para unitários;
- [ ] nenhum secret entra na imagem.

## Evidências

Preencher ao executar a task:

- Branch:
- Commits:
- Testes antes:
- Testes depois:
- Lint:
- Type-check:
- Observações:
