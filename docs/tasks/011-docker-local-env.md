# Docker e ambiente local

Status: `CONCLUÍDA`

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
- [x] backend sobe em container;
- [x] banco local opcional sobe via compose;
- [x] migration executa no fluxo configurado até `head`;
- [x] Swagger responde no container;
- [x] testes não dependem do container para unitários;
- [x] nenhum secret entra na imagem.

## Evidências

Preencher ao executar a task:

- Branch: `chore/docker-ambiente-local`
- Commits: `b7dd2db` (`chore: padroniza ambiente local com Docker`) e `a58c52a`
  (`docs: registra ambiente Docker local`)
- Testes antes: `117 passed`; cobertura total de `94%`
- Testes depois: `120 passed`; cobertura total de `94%`
- Lint: Ruff e formatter Ruff aprovados
- Type-check: `mypy backend` aprovado em 52 arquivos
- Docker: Engine `29.7.2` e Compose `v5.4.0`
- Build: imagem do backend construída com sucesso
- Serviços: PostgreSQL e backend saudáveis via Compose
- Migration: `d7e9f2a3b4c5 (head)` aplicada no PostgreSQL do container
- Runtime: backend executado como `uid=999(railops)`
- HTTP: `/health` retornou `{"status":"ok"}`, `/docs` retornou HTTP 200 e o
  OpenAPI respondeu com o título `RailOps API`
- Observações: Dockerfile multi-stage, usuário não-root, healthcheck,
  `.dockerignore`, Compose com PostgreSQL e variáveis externas implementados.
  Os testes unitários continuam independentes do Docker. Os containers foram
  encerrados após a validação e os volumes locais foram preservados.

## Roteiro de validação manual

```powershell
Copy-Item .env.docker.example .env.docker
docker compose --env-file .env.docker up --build -d
docker compose --env-file .env.docker ps
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-WebRequest http://127.0.0.1:8000/docs
docker compose --env-file .env.docker down
```

O roteiro acima foi executado com sucesso em 21/08/2026.
