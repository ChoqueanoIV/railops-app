# Documentação técnica — RailOps

Este diretório organiza a evolução técnica do `railops-app`.

## Índice

- [`CHECKPOINT.md`](CHECKPOINT.md) — estado seguro e próximo passo.
- [`ROADMAP.md`](ROADMAP.md) — sequência proposta para a segunda fase.
- [`validation/019-technical-homologation.md`](validation/019-technical-homologation.md)
  — resultado técnico e pendências da homologação atual.
- [`architecture/current-state.md`](architecture/current-state.md) — estado
  implementado e validado.
- [`architecture/baseline.md`](architecture/baseline.md) — regras de negócio
  protegidas pela caracterização.
- [`architecture/target-architecture.md`](architecture/target-architecture.md)
  — arquitetura alvo.
- [`architecture/migration-strategy.md`](architecture/migration-strategy.md) —
  migração incremental sem big bang.
- [`standards/api.md`](standards/api.md) — padrão REST.
- [`standards/backend.md`](standards/backend.md) — padrões Python/FastAPI.
- [`standards/frontend.md`](standards/frontend.md) — padrões React/TypeScript.
- [`standards/testing.md`](standards/testing.md) — estratégia de testes.
- [`standards/dependencies.md`](standards/dependencies.md) — dependências.
- [`standards/git.md`](standards/git.md) — commits e entrega.
- [`adr/README.md`](adr/README.md) — decisões arquiteturais aceitas e sua
  governança.
- [`tasks/README.md`](tasks/README.md) — backlog executável.

Para instalar e executar o sistema, incluindo Docker, frontend React, usuário
de demonstração e troubleshooting, consulte o [`README principal`](../README.md).

## Estado resumido

- backend FastAPI organizado por features, com PostgreSQL e Alembic;
- frontend React com autenticação e fluxos de Brisamar e TECON;
- 133 testes backend, 13 testes frontend e cobertura backend de 94,06%;
- lint, formatter, type-check, build, pre-commit, Docker e CI validados;
- legado e adaptadores preservados temporariamente para uma remoção segura;
- sem deploy público, consulta de histórico, filtros, exportações ou relatórios.

## Como executar o plano

1. Comece por [`tasks/README.md`](tasks/README.md).
2. Trabalhe em apenas uma task por vez.
3. Crie branch específica.
4. Peça ao Codex para ler `AGENTS.md` e a task.
5. Execute testes antes e depois.
6. Faça commit semântico.
7. Atualize a task com evidências.

## Qualidade do backend

O projeto usa Python 3.13 e `uv.lock` como fonte reproduzível das versões. No
Windows, instale o `uv` no perfil do usuário e reabra o terminal:

```powershell
py -3.13 -m pip install --user uv
```

Na raiz do repositório, reconstrua o ambiente exatamente como registrado no
lockfile:

```powershell
py -3.13 -m uv sync --frozen
```

Execute os checks pelo ambiente gerenciado:

```powershell
py -3.13 -m uv run pytest
py -3.13 -m uv run pytest --cov=backend/app --cov-report=term-missing
py -3.13 -m uv run pytest -m unit
py -3.13 -m uv run pytest -m integration
py -3.13 -m uv run pytest -m api
py -3.13 -m uv run ruff check .
py -3.13 -m uv run ruff format --check .
py -3.13 -m uv run mypy
py -3.13 -m uv run pre-commit run --all-files
```

Para instalar os hooks locais do Git:

```powershell
py -3.13 -m uv run pre-commit install
py -3.13 -m uv run pre-commit install --hook-type pre-push
```

### Compatibilidade com pip

Os arquivos `backend/requirements.txt` e `backend/requirements-dev.txt` são
exports gerados do mesmo `uv.lock`, com hashes. Eles permanecem disponíveis
durante a transição para ferramentas que ainda usam `pip`:

```powershell
py -3.13 -m venv .venv
.venv\Scripts\python.exe -m pip install --require-hashes -r backend\requirements-dev.txt
```

Não edite os requirements manualmente. Após uma alteração intencional no
manifesto, regenere-os com:

```powershell
py -3.13 -m uv lock
py -3.13 -m uv export --locked --no-default-groups --no-dev --no-emit-project --format requirements.txt --output-file backend\requirements.txt
py -3.13 -m uv export --locked --no-default-groups --group dev --no-emit-project --format requirements.txt --output-file backend\requirements-dev.txt
```

Se o Windows bloquear executáveis criados dentro do OneDrive, mantenha o clone
do projeto em uma pasta local não sincronizada.

## Configuração do backend

Copie `backend/.env.example` para `backend/.env` e substitua os valores locais.
O arquivo `.env` real permanece ignorado pelo Git.

- `DATABASE_URL`: conexão PostgreSQL obrigatória;
- `JWT_SECRET_KEY`: segredo JWT obrigatório; em `production`, mínimo de 32
  bytes;
- `RAILOPS_ENV`: `development`, `test` ou `production` (padrão: `development`);
- `API_TITLE`: título exibido no OpenAPI (padrão: `RailOps API`);
- `CORS_ORIGINS`: origens permitidas separadas por vírgula.

Em `production`, `CORS_ORIGINS` não aceita `*`. `/health` verifica o processo e
`/ready` verifica a conexão com o banco sem expor dados internos. Respostas
incluem `X-Request-ID`; logs estruturados não registram payloads ou credenciais.

O entrypoint recomendado é `app.main:app` a partir da pasta `backend`. O
entrypoint anterior `main:app` permanece compatível durante a migração.
