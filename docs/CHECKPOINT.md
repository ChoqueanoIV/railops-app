# Checkpoint de continuidade — RailOps

Atualizado em: 21/08/2026

## Estado seguro atual

- branch de continuidade: `main`;
- PR funcional mais recente: [#31 — shell React + TypeScript](https://github.com/ChoqueanoIV/railops-app/pull/31), mesclada;
- merge funcional consolidado na `main`: `30e3890`;
- nenhuma implementação pendente fora da `main`;
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

## Validação da task 012

- `npm run dev` respondeu HTTP 200;
- build Vite aprovado;
- ESLint e Prettier aprovados;
- type-check TypeScript aprovado;
- 2 testes Vitest aprovados;
- auditoria npm sem vulnerabilidades;
- 120 testes do backend aprovados;
- Ruff, formatter Ruff, mypy e pre-commit aprovados;
- nenhum HTML, CSS ou JavaScript legado alterado;
- nenhuma regra de negócio ou contrato HTTP alterado.

## O que foi entregue na task 012

- shell React + TypeScript isolado em `frontend/react`;
- Vite, React Router, ESLint, Prettier, Vitest e Testing Library;
- alias `@/` e estrutura inicial feature-first;
- `.env.example`, scripts de qualidade e lockfile reproduzível;
- frontend legado preservado e ainda executável durante a transição;
- instruções de execução e estado arquitetural atualizados.

## Próximo passo obrigatório

1. confirmar worktree limpo;
2. ler `AGENTS.md` e `docs/tasks/013-react-api-auth.md`;
3. executar o baseline completo;
4. executar somente a task 013.

Não combinar a task 013 com tasks posteriores.

## Restrições de continuidade

- preservar integralmente as regras de negócio registradas em
  `docs/architecture/baseline.md`;
- não alterar contratos HTTP fora dos critérios explícitos da task 013;
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
