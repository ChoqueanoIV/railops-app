# Documentação técnica — RailOps

Este diretório organiza a evolução técnica do `railops-app`.

## Índice

- `architecture/current-state.md` — leitura do estado atual.
- `architecture/target-architecture.md` — arquitetura alvo.
- `architecture/migration-strategy.md` — como migrar sem big bang.
- `standards/api.md` — padrão REST.
- `standards/backend.md` — padrões Python/FastAPI.
- `standards/frontend.md` — padrões React/TypeScript.
- `standards/testing.md` — estratégia de testes.
- `standards/dependencies.md` — gestão de dependências.
- `standards/git.md` — commits e entrega.
- `tasks/` — backlog executável para o Codex.

## Como executar o plano

1. Comece por `tasks/README.md`.
2. Trabalhe em apenas uma task por vez.
3. Crie branch específica.
4. Peça ao Codex para ler `AGENTS.md` e a task.
5. Execute testes antes e depois.
6. Faça commit semântico.
7. Atualize a task com evidências.

## Qualidade do backend

Instale as dependências de desenvolvimento a partir da raiz do repositório:

```bash
python -m pip install -r backend/requirements-dev.txt
```

Execute os checks também a partir da raiz:

```bash
python -m pytest
python -m pytest --cov=backend/app --cov-report=term-missing
python -m ruff check .
python -m ruff format --check .
python -m mypy
python -m pre_commit run --all-files
```

Para instalar os hooks locais do Git:

```bash
python -m pre_commit install
python -m pre_commit install --hook-type pre-push
```
