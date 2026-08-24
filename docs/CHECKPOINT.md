# Checkpoint de continuidade — RailOps

Atualizado em: 23/08/2026

## Estado seguro atual

- branch de continuidade: `feat/react-api-auth`;
- PR em revisão: [#32 — autenticação no React](https://github.com/ChoqueanoIV/railops-app/pull/32), com base em `main`;
- checkpoint da `main` anterior à PR: `fa7d83c`;
- implementação e documentação da task 013 concluídas, aguardando merge;
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
- 011 — Docker e ambiente local: integrada no PR #30.
- 012 — shell React + TypeScript: integrada no PR #31.

## Task em revisão

- 013 — cliente API e autenticação no React: concluída no PR #32, aguardando
  revisão e merge.

## Validação da task 013

- 10 testes React aprovados;
- build Vite aprovado;
- ESLint e Prettier aprovados;
- type-check TypeScript aprovado;
- servidor Vite respondeu HTTP 200;
- 120 testes do backend aprovados;
- Ruff, formatter Ruff, mypy e pre-commit aprovados;
- nenhum arquivo do backend ou frontend legado alterado;
- nenhuma regra de negócio ou contrato HTTP alterado.

## O que foi entregue na task 013

- cliente HTTP central tipado com base URL por ambiente e timeout;
- headers JSON e bearer normalizados;
- parsing controlado do envelope de erro e tratamento de 401/403;
- login e primeiro acesso integrados aos contratos existentes;
- sessão JWT em `sessionStorage`, logout e rotas protegidas;
- testes dos fluxos críticos e documentação atualizada.

## Próximo passo obrigatório

1. revisar e mesclar o PR #32;
2. sincronizar a `main` local com `origin/main`;
3. confirmar worktree limpo;
4. ler `AGENTS.md` e `docs/tasks/014-react-screen-migration.md`;
5. executar o baseline completo;
6. executar somente a task 014.

Não iniciar a task 014 antes do merge do PR #32 nem combiná-la com tasks
posteriores.

## Restrições de continuidade

- preservar integralmente as regras de negócio registradas em
  `docs/architecture/baseline.md`;
- não alterar contratos HTTP fora dos critérios explícitos da task 014;
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
