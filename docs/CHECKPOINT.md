# Checkpoint de continuidade — RailOps

Atualizado em: 18/08/2026

## Estado seguro atual

- branch de trabalho: `refactor/typed-config-bootstrap`;
- pull request aberto: [#22 — configuração tipada e bootstrap](https://github.com/ChoqueanoIV/railops-app/pull/22);
- base do PR: `main`;
- PR sem conflitos e pronto para merge automático;
- `main` remota antes do PR #22: merge `b8fe079`;
- nenhuma alteração local pendente antes da criação deste checkpoint;
- autoria Git configurada como `Leandro CHOQUE <leandro.cristine1@gmail.com>`.

## Tasks concluídas

- 001 — baseline e testes de caracterização: integrada no PR #19;
- 002 — tooling Python e `pyproject.toml`: integrada no PR #20;
- 003 — dependências reproduzíveis: integrada no PR #21;
- 004 — configuração tipada e bootstrap: implementação concluída no PR #22,
  aguardando merge.

## Validação da task 004

- 105 testes aprovados;
- cobertura total de 94%;
- `ruff check .` aprovado;
- `ruff format --check .` aprovado;
- `mypy` aprovado em 22 arquivos de produção;
- pre-commit aprovado;
- inventário, autenticação e respostas OpenAPI preservados;
- Swagger mantido em `/docs`;
- nenhuma regra de negócio ou contrato HTTP alterado.

## O que foi entregue na task 004

- configuração tipada e imutável em `backend/app/core/config.py`;
- variáveis de banco, JWT, ambiente, título e CORS centralizadas;
- fábrica `criar_app` e bootstrap em `backend/app/main.py`;
- compatibilidade temporária mantida em `backend/main.py`;
- `backend/.env.example` sem credenciais reais;
- testes isolados do `.env` local;
- documentação do estado atual atualizada.

## Próximo passo obrigatório

1. revisar o PR #22;
2. fazer o merge somente se ele continuar sem conflitos;
3. sincronizar a `main` local com `origin/main`;
4. confirmar worktree limpo;
5. ler e executar somente `docs/tasks/005-api-response-errors.md`.

Não iniciar a task 005 antes do merge e da sincronização da task 004.

## Restrições de continuidade

- preservar integralmente as regras de negócio registradas em
  `docs/architecture/baseline.md`;
- não alterar contratos HTTP fora dos critérios explícitos da task 005;
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
