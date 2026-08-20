# Checkpoint de continuidade — RailOps

Atualizado em: 19/08/2026

## Estado seguro atual

- branch de trabalho: `refactor/auth-feature`;
- pull request aberto: [#24 — autenticação por feature](https://github.com/ChoqueanoIV/railops-app/pull/24);
- base do PR: `main`;
- PR sem conflitos e pronto para merge automático;
- `main` remota antes do PR #24: merge `abc9c0a`;
- nenhuma alteração local pendente antes da criação deste checkpoint;
- autoria Git configurada como `Leandro CHOQUE <leandro.cristine1@gmail.com>`.

## Tasks concluídas

- 001 — baseline e testes de caracterização: integrada no PR #19;
- 002 — tooling Python e `pyproject.toml`: integrada no PR #20;
- 003 — dependências reproduzíveis: integrada no PR #21;
- 004 — configuração tipada e bootstrap: integrada no PR #22;
- 005 — contrato de erros e responses: integrada no PR #23;
- 006 — arquitetura de autenticação por feature: implementação concluída no
  PR #24, aguardando merge.

## Validação da task 006

- 110 testes aprovados;
- cobertura total de 94%;
- `ruff check backend` aprovado;
- formatter Ruff aprovado;
- `mypy` aprovado no escopo configurado;
- pre-commit aprovado;
- matrícula, PIN, JWT HS256, claims e expiração preservados;
- primeiro acesso e contratos HTTP preservados;
- Swagger mantido em `/docs`;
- nenhuma regra de negócio alterada; compatibilidade HTTP legada preservada.

## O que foi entregue na task 006

- feature canônica em `backend/app/features/auth`;
- controller limitado à borda HTTP;
- service desacoplado do banco por `UsuarioRepositoryProtocol`;
- repository e modelo ORM organizados dentro da feature;
- dependencies, exceptions, schemas e tipos isolados;
- adaptadores temporários para os imports antigos;
- teste que garante reexportação sem duplicar modelos ou contratos.

## Próximo passo obrigatório

1. revisar o PR #24;
2. fazer o merge somente se ele continuar sem conflitos;
3. sincronizar a `main` local com `origin/main`;
4. confirmar worktree limpo;
5. ler e executar somente `docs/tasks/007-backend-passagens-feature.md`.

Não iniciar a task 007 antes do merge e da sincronização da task 006.

## Restrições de continuidade

- preservar integralmente as regras de negócio registradas em
  `docs/architecture/baseline.md`;
- não alterar contratos HTTP fora dos critérios explícitos da task 007;
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
