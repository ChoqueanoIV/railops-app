# Checkpoint de continuidade — RailOps

Atualizado em: 21/08/2026

## Estado seguro atual

- branch de continuidade: `chore/docker-ambiente-local`;
- PR em revisão: [#30 — ambiente Docker local](https://github.com/ChoqueanoIV/railops-app/pull/30), com base em `main`;
- checkpoint da `main` anterior à PR: `fa762e6`;
- implementação e documentação da task 011 concluídas, aguardando merge;
- worktree limpo antes da atualização deste checkpoint documental;
- autoria Git configurada como `Leandro CHOQUE <leandro.cristine1@gmail.com>`.

## Tasks concluídas

- 001 — baseline e testes de caracterização: integrada no PR #19;
- 002 — tooling Python e `pyproject.toml`: integrada no PR #20;
- 003 — dependências reproduzíveis: integrada no PR #21;
- 004 — configuração tipada e bootstrap: integrada no PR #22;
- 005 — contrato de erros e responses: integrada no PR #23;
- 006 — arquitetura de autenticação por feature: integrada no PR #24;
- 007 — arquitetura de passagens por feature: integrada no PR #25;
- 008 — repositories e fronteira transacional: integrada no PR #26.
- 009 — tipagem progressiva do backend: integrada no PR #28.
- 010 — reorganização dos testes e cobertura: integrada no PR #29.

## Task em revisão

- 011 — Docker e ambiente local: concluída no PR #30, aguardando revisão e
  merge.

## Validação da task 011

- 120 testes aprovados;
- cobertura total de 94%;
- `ruff check backend` aprovado;
- formatter Ruff aprovado;
- `mypy backend` aprovado em 52 arquivos;
- pre-commit aprovado;
- imagem do backend construída com Docker Engine 29.7.2 e Compose v5.4.0;
- PostgreSQL e backend saudáveis no Compose;
- migrations aplicadas até `d7e9f2a3b4c5 (head)`;
- backend executado como usuário não-root `uid=999(railops)`;
- `/health` aprovado, `/docs` retornou HTTP 200 e OpenAPI identificado como
  `RailOps API`;
- nenhuma regra de negócio ou contrato HTTP alterado.

## O que foi entregue na task 011

- Dockerfile multi-stage para o backend com usuário não-root;
- `.dockerignore` e configuração externa de ambiente;
- PostgreSQL opcional via Docker Compose;
- healthchecks do banco e da API;
- migrations Alembic antes da inicialização do Uvicorn;
- instruções de execução, validação e solução de problemas documentadas.

## Próximo passo obrigatório

1. revisar e mesclar o PR #30;
2. sincronizar a `main` local com `origin/main`;
3. confirmar worktree limpo;
4. ler `AGENTS.md` e `docs/tasks/012-react-shell.md`;
5. executar o baseline completo;
6. executar somente a task 012.

Não iniciar a task 012 antes do merge do PR #30 nem combiná-la com tasks
posteriores.

## Restrições de continuidade

- preservar integralmente as regras de negócio registradas em
  `docs/architecture/baseline.md`;
- não alterar contratos HTTP fora dos critérios explícitos da task 012;
- manter commits em PT-BR e sem marcadores de coautoria por IA;
- nunca versionar `.env`, tokens, URLs privadas ou credenciais;
- executar testes antes e depois de qualquer refatoração.

## Ambiente local no Windows

O executável Python dentro do `venv` no OneDrive pode ser bloqueado. Quando
isso ocorrer, use o Python 3.13 instalado no perfil com os pacotes do ambiente:

```powershell
$env:PYTHONPATH=(Resolve-Path 'venv/Lib/site-packages').Path
& 'C:\Users\Leandro CHOQUE\AppData\Local\Programs\Python\Python313\python.exe' -m pytest
```

Para uma reconstrução limpa, o fluxo preferencial está documentado em
`docs/README.md` e usa `uv sync --frozen`.
