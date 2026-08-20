# Checkpoint de continuidade — RailOps

Atualizado em: 19/08/2026

## Estado seguro atual

- branch de trabalho: `refactor/api-response-errors`;
- pull request aberto: [#23 — contratos de erro da API](https://github.com/ChoqueanoIV/railops-app/pull/23);
- base do PR: `main`;
- PR sem conflitos e pronto para merge automático;
- `main` remota antes do PR #23: merge `3c1b1c9`;
- nenhuma alteração local pendente antes da criação deste checkpoint;
- autoria Git configurada como `Leandro CHOQUE <leandro.cristine1@gmail.com>`.

## Tasks concluídas

- 001 — baseline e testes de caracterização: integrada no PR #19;
- 002 — tooling Python e `pyproject.toml`: integrada no PR #20;
- 003 — dependências reproduzíveis: integrada no PR #21;
- 004 — configuração tipada e bootstrap: integrada no PR #22;
- 005 — contrato de erros e responses: implementação concluída no PR #23,
  aguardando merge.

## Validação da task 005

- 109 testes aprovados;
- cobertura total de 94%;
- `ruff check backend` aprovado;
- formatter Ruff aprovado;
- `mypy` aprovado no escopo configurado;
- pre-commit aprovado;
- status HTTP, `detail` legado e corpos de sucesso preservados;
- erros conhecidos documentados no OpenAPI;
- Swagger mantido em `/docs`;
- nenhuma regra de negócio alterada; compatibilidade HTTP legada preservada.

## O que foi entregue na task 005

- envelope tipado `error.code/message/details` para erros da API;
- campo `detail` mantido durante a transição do frontend legado;
- exception handlers centralizados em `backend/app/api/errors.py`;
- routers sem dependência direta de `HTTPException` para erros conhecidos;
- códigos estáveis para autenticação, validação e passagens;
- summaries e responses relevantes registrados no OpenAPI;
- documentação dos contratos e evidências atualizada.

## Próximo passo obrigatório

1. revisar o PR #23;
2. fazer o merge somente se ele continuar sem conflitos;
3. sincronizar a `main` local com `origin/main`;
4. confirmar worktree limpo;
5. ler e executar somente `docs/tasks/006-backend-auth-feature.md`.

Não iniciar a task 006 antes do merge e da sincronização da task 005.

## Restrições de continuidade

- preservar integralmente as regras de negócio registradas em
  `docs/architecture/baseline.md`;
- não alterar contratos HTTP fora dos critérios explícitos da task 006;
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
