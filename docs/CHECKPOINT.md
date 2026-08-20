# Checkpoint de continuidade — RailOps

Atualizado em: 19/08/2026

## Estado seguro atual

- branch de trabalho: `refactor/passagens-feature`;
- pull request aberto: [#25 — passagens por feature](https://github.com/ChoqueanoIV/railops-app/pull/25);
- base do PR: `main`;
- PR sem conflitos e pronto para merge automático;
- `main` remota antes do PR #25: merge `eee5705`;
- nenhuma alteração local pendente antes da criação deste checkpoint;
- autoria Git configurada como `Leandro CHOQUE <leandro.cristine1@gmail.com>`.

## Tasks concluídas

- 001 — baseline e testes de caracterização: integrada no PR #19;
- 002 — tooling Python e `pyproject.toml`: integrada no PR #20;
- 003 — dependências reproduzíveis: integrada no PR #21;
- 004 — configuração tipada e bootstrap: integrada no PR #22;
- 005 — contrato de erros e responses: integrada no PR #23;
- 006 — arquitetura de autenticação por feature: integrada no PR #24;
- 007 — arquitetura de passagens por feature: implementação concluída no PR
  #25, aguardando merge.

## Validação da task 007

- 111 testes aprovados;
- cobertura total de 94%;
- `ruff check backend` aprovado;
- formatter Ruff aprovado;
- `mypy` aprovado no escopo configurado;
- pre-commit aprovado;
- regras de Brisamar, TECON, edição e histórico preservadas;
- contratos HTTP e transações preservados;
- Swagger mantido em `/docs`;
- nenhuma regra de negócio alterada; compatibilidade HTTP legada preservada.

## O que foi entregue na task 007

- feature canônica em `backend/app/features/passagens`;
- controller limitado à borda HTTP;
- models, repository, schemas, service e exceptions organizados na feature;
- fluxos Brisamar e TECON mantidos explícitos, sem herança artificial;
- adaptadores temporários para os imports antigos;
- teste que garante reexportação sem duplicar modelos ORM ou contratos.

## Próximo passo obrigatório

1. revisar o PR #25;
2. fazer o merge somente se ele continuar sem conflitos;
3. sincronizar a `main` local com `origin/main`;
4. confirmar worktree limpo;
5. ler e executar somente `docs/tasks/008-repositories-transactions.md`.

Não iniciar a task 008 antes do merge e da sincronização da task 007.

## Restrições de continuidade

- preservar integralmente as regras de negócio registradas em
  `docs/architecture/baseline.md`;
- não alterar contratos HTTP fora dos critérios explícitos da task 008;
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
