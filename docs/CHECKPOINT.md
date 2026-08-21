# Checkpoint de continuidade — RailOps

Atualizado em: 21/08/2026

## Estado seguro atual

- branch de continuidade: `test/reorganiza-suite-cobertura`;
- PR aberta: [#29 — reorganização da suíte e cobertura](https://github.com/ChoqueanoIV/railops-app/pull/29);
- base da PR: `main`;
- checkpoint consolidado na `main` antes da PR: `b1cdd39`;
- implementação e documentação da task 010 concluídas, aguardando merge;
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

## Task em revisão

- 010 — reorganização dos testes e cobertura: implementação concluída no PR
  #29, aguardando merge.

## Validação da task 010

- 117 testes aprovados;
- cobertura total de 94%;
- 83 testes unitários, 13 de integração e 21 de API aprovados isoladamente;
- `ruff check backend` aprovado;
- formatter Ruff aprovado;
- `mypy backend` aprovado em 52 arquivos;
- pre-commit aprovado;
- nenhuma linha da aplicação, regra de negócio ou contrato HTTP alterado.

## O que foi entregue na task 010

- suíte organizada em pacotes `unit`, `integration`, `api` e `fixtures`;
- markers registrados para execução seletiva dos três grupos;
- fixtures tipadas de configuração da aplicação e banco de teste;
- proteção explícita contra configuração do banco de produção;
- relatório de cobertura de statements e branches preservado;
- comandos e estratégia de testes documentados.

## Próximo passo obrigatório

1. revisar e mesclar o PR #29;
2. sincronizar a `main` local com `origin/main`;
3. confirmar worktree limpo;
4. ler `AGENTS.md` e `docs/tasks/011-docker-local-env.md`;
5. executar o baseline completo;
6. executar somente a task 011.

Não iniciar a task 011 antes do merge da task 010 e não combiná-la com tasks
posteriores.

## Restrições de continuidade

- preservar integralmente as regras de negócio registradas em
  `docs/architecture/baseline.md`;
- não alterar contratos HTTP fora dos critérios explícitos da task 011;
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
