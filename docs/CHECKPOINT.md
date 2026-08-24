# Checkpoint de continuidade — RailOps

Atualizado em: 24/08/2026

## Estado seguro atual

- branch funcional atual: `feat/migra-telas-react`;
- PR funcional mais recente: [#32 — autenticação no React](https://github.com/ChoqueanoIV/railops-app/pull/32), mesclada;
- merge funcional consolidado na `main`: `192fe1e`;
- implementação da task 014 pronta para revisão e abertura de PR;
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
- 014 — migração incremental das telas: concluída na branch
  `feat/migra-telas-react`, aguardando PR.

## Validação da task 014

- 13 testes React aprovados;
- build Vite aprovado;
- ESLint e Prettier aprovados;
- type-check TypeScript aprovado;
- servidor Vite respondeu HTTP 200;
- 120 testes do backend aprovados;
- Ruff, formatter Ruff, mypy e pre-commit aprovados;
- nenhum arquivo do backend ou frontend legado alterado ou removido;
- nenhuma regra de negócio ou contrato HTTP alterado.

## O que foi entregue na task 014

- seleção de Brisamar ou TECON após autenticação;
- formulários React tipados para os dois terminais;
- criação e edição conectadas ao cliente HTTP central;
- campos imutáveis preservados na edição;
- estados de carregamento, erro, envio e confirmação;
- legado preservado como fallback para validação operacional.

## Próximo passo obrigatório

1. revisar o diff e publicar a branch `feat/migra-telas-react`;
2. abrir e revisar o PR da task 014;
3. mesclar somente após checks verdes;
4. criar checkpoint na `main` e iniciar somente a task 015.

Não combinar a task 015 com tasks posteriores.

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
