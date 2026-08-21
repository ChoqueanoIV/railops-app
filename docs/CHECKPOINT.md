# Checkpoint de continuidade — RailOps

Atualizado em: 21/08/2026

## Estado seguro atual

- branch de continuidade: `refactor/backend-typing`;
- PR funcional aberta: [#28 — tipagem progressiva do backend](https://github.com/ChoqueanoIV/railops-app/pull/28);
- base da PR: `main`;
- merge consolidado na `main` antes da PR: `0b9a971`;
- implementação e documentação da task 009 concluídas, aguardando revisão e merge;
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

## Task em revisão

- 009 — tipagem progressiva do backend: implementação concluída no PR #28,
  aguardando merge.

## Validação da task 009

- 116 testes aprovados;
- cobertura total de 94%;
- `ruff check backend` aprovado;
- formatter Ruff aprovado;
- `mypy` aprovado em 45 arquivos, com `disallow_untyped_defs = true` e sem
  exceções por módulo;
- pre-commit aprovado;
- nenhuma regra de negócio ou contrato HTTP alterado.

## O que foi entregue na task 009

- assinaturas completas obrigatórias no código de produção;
- remoção dos overrides de `mypy` por módulo;
- controllers, validators, repositories e service de passagens tipados;
- schemas tipados para respostas de equipe, linhas, rádios e detalhes dos
  terminais Brisamar e TECON;
- unions, mapas, snapshots e retornos internos com tipos concretos;
- nenhum `Any`, cast ou `type: ignore` introduzido.

## Próximo passo obrigatório

1. revisar e mesclar o PR #28;
2. sincronizar a `main` local com `origin/main`;
3. confirmar worktree limpo;
4. ler `AGENTS.md` e `docs/tasks/010-tests-structure-coverage.md`;
5. executar o baseline completo;
6. executar somente a task 010.

Não iniciar a task 010 antes do merge da task 009 e não combiná-la com tasks
posteriores.

## Restrições de continuidade

- preservar integralmente as regras de negócio registradas em
  `docs/architecture/baseline.md`;
- não alterar contratos HTTP fora dos critérios explícitos da task 010;
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
