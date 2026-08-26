# Checkpoint de continuidade — RailOps

Atualizado em: 25/08/2026

## Estado seguro atual

- branch funcional atual: `ci/qualidade-pr`;
- PR em revisão: [#34 — CI de qualidade](https://github.com/ChoqueanoIV/railops-app/pull/34), com jobs de backend e frontend aprovados;
- PR funcional mais recente: [#33 — migração das passagens para React](https://github.com/ChoqueanoIV/railops-app/pull/33), mesclada;
- merge funcional consolidado na `main`: `ad88f08`;
- implementação da task 015 pronta para merge no PR #34;
- commit funcional da task 015: `1bd6321`;
- commit funcional da task 014: `1a5c0bf`;
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
- 013 — cliente API e autenticação no React: integrada no PR #32.
- 014 — migração incremental das telas: integrada no PR #33.
- 015 — CI de qualidade: concluída na branch `ci/qualidade-pr`, aguardando
  merge do PR #34.

## Validação da task 015

- jobs remotos `Backend` e `Frontend` aprovados na primeira execução;
- 123 testes do backend e 13 testes React aprovados;
- build Vite aprovado;
- ESLint e Prettier aprovados;
- type-check TypeScript aprovado;
- cobertura real de `93,70%`, reportada de forma arredondada como `94%`;
- Ruff, formatter Ruff, mypy e pre-commit aprovados;
- nenhum arquivo de produção alterado;
- nenhuma regra de negócio ou contrato HTTP alterado.

## O que foi entregue na task 015

- workflow para pull requests e `main`;
- jobs independentes para backend e frontend;
- instalação reproduzível a partir dos dois lockfiles;
- PostgreSQL efêmero e ambiente de testes sem secrets reais;
- lint, formatação, type-check, testes, cobertura e build bloqueantes;
- testes estruturais do contrato de CI.

## Próximo passo obrigatório

1. revisar e mesclar o PR #34;
2. sincronizar a `main` e criar o checkpoint pós-merge;
3. ler `AGENTS.md` e `docs/tasks/016-readme-docs.md`;
4. executar somente a task 016.

Não iniciar a task 016 antes do merge e do checkpoint da task 015.

## Restrições de continuidade

- preservar integralmente as regras de negócio registradas em
  `docs/architecture/baseline.md`;
- não alterar contratos HTTP fora dos critérios explícitos da task 015;
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
