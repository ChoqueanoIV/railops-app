# Docker e ambiente local

Status: `IMPLEMENTADA — VALIDAÇÃO DOCKER PENDENTE`

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
- [x] migration executa no fluxo configurado e gera SQL offline até `head`;
- [ ] Swagger responde no container;
- [x] testes não dependem do container para unitários;
- [x] nenhum secret entra na imagem.

## Evidências

Preencher ao executar a task:

- Branch: `chore/docker-ambiente-local`
- Commits: `b7dd2db` (`chore: padroniza ambiente local com Docker`)
- Testes antes: `117 passed`; cobertura total de `94%`
- Testes depois: `120 passed`; cobertura total de `94%`
- Lint: Ruff e formatter Ruff aprovados
- Type-check: `mypy backend` aprovado em 52 arquivos
- Migration: `alembic upgrade head --sql` aprovado para toda a cadeia
- Observações: Dockerfile multi-stage, usuário não-root, healthcheck,
  `.dockerignore`, Compose com PostgreSQL e variáveis externas implementados.
  O Docker não está instalado no ambiente atual; por isso build, subida real,
  healthcheck e Swagger no container permanecem como validação obrigatória.

## Validação pendente em máquina com Docker

```powershell
Copy-Item .env.docker.example .env.docker
docker compose --env-file .env.docker up --build -d
docker compose --env-file .env.docker ps
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-WebRequest http://127.0.0.1:8000/docs
docker compose --env-file .env.docker down
```

Só alterar o status para `CONCLUÍDA` depois que os serviços aparecerem
saudáveis, a migration terminar sem erro e `/docs` responder HTTP 200.
