# Checkpoint de continuidade — RailOps

Atualizado em: 20/08/2026

## Estado seguro atual

- branch de trabalho: `refactor/repositories-transactions`;
- pull request aberto: [#26 — fronteira transacional](https://github.com/ChoqueanoIV/railops-app/pull/26);
- base do PR: `main`;
- PR sem conflitos e pronto para merge automático;
- `main` remota antes do PR #26: merge `01a94df`;
- nenhuma alteração local pendente antes da criação deste checkpoint;
- autoria Git configurada como `Leandro CHOQUE <leandro.cristine1@gmail.com>`.

## Tasks concluídas

- 001 — baseline e testes de caracterização: integrada no PR #19;
- 002 — tooling Python e `pyproject.toml`: integrada no PR #20;
- 003 — dependências reproduzíveis: integrada no PR #21;
- 004 — configuração tipada e bootstrap: integrada no PR #22;
- 005 — contrato de erros e responses: integrada no PR #23;
- 006 — arquitetura de autenticação por feature: integrada no PR #24;
- 007 — arquitetura de passagens por feature: integrada no PR #25;
- 008 — repositories e fronteira transacional: implementação concluída no PR
  #26, aguardando merge.

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

1. revisar o PR #26;
2. fazer o merge somente se ele continuar sem conflitos;
3. sincronizar a `main` local com `origin/main`;
4. confirmar worktree limpo;
5. ler e executar somente `docs/tasks/009-backend-typing.md`.

Não iniciar a task 009 antes do merge e da sincronização da task 008.

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
