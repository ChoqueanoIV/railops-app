# Checkpoint de continuidade — RailOps

Atualizado em: 20/08/2026

## Estado seguro atual

- branch de continuidade: `main`;
- PR funcional mais recente: [#26 — fronteira transacional](https://github.com/ChoqueanoIV/railops-app/pull/26), mesclada;
- merge funcional consolidado na `main`: `b988b08`;
- nenhuma implementação pendente fora da `main`;
- worktree limpo antes da criação deste checkpoint documental;
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

## Validação da task 008

- 115 testes aprovados;
- cobertura total de 94%;
- `ruff check backend` aprovado;
- formatter Ruff aprovado;
- `mypy` aprovado no escopo configurado;
- pre-commit aprovado;
- regras e contratos HTTP preservados;
- PostgreSQL, metadata e Alembic preservados;
- Swagger mantido em `/docs`;
- nenhuma regra de negócio alterada; compatibilidade HTTP legada preservada.

## O que foi entregue na task 008

- `TransacaoSQLAlchemy` centralizando commit, rollback e refresh;
- uma sessão compartilhada por requisição;
- services injetados nos controllers, sem SQLAlchemy na borda HTTP;
- falhas de banco convertidas em `PERSISTENCE_ERROR` neutro;
- responsabilidades documentadas em `docs/architecture/transactions.md`;
- testes específicos da fronteira transacional e do tratamento HTTP.

## Próximo passo obrigatório

1. sincronizar a `main` local com `origin/main`;
2. confirmar worktree limpo;
3. ler `AGENTS.md` e `docs/tasks/009-backend-typing.md`;
4. executar o baseline completo;
5. executar somente a task 009.

Não combinar a task 009 com tasks posteriores.

## Restrições de continuidade

- preservar integralmente as regras de negócio registradas em
  `docs/architecture/baseline.md`;
- não alterar contratos HTTP fora dos critérios explícitos da task 009;
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
