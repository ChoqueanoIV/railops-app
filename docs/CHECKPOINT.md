# Checkpoint de continuidade — RailOps

Atualizado em: 25/08/2026

## Estado seguro atual

- branch de continuidade: `main`;
- PR mais recente: [#35 — README e documentação final](https://github.com/ChoqueanoIV/railops-app/pull/35), mesclada;
- merge consolidado na `main`: `2d4d2c5`;
- nenhuma implementação pendente fora da `main`;
- worktree limpo antes da atualização deste checkpoint documental;
- commit principal da task 016: `e8047ab`;
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
- 015 — CI de qualidade: integrada no PR #34.
- 016 — README e documentação final: integrada no PR #35.

## Validação da task 016

- jobs remotos `Backend` e `Frontend` aprovados no PR;
- 123 testes do backend e 13 testes React aprovados;
- build Vite aprovado;
- ESLint e Prettier aprovados;
- type-check TypeScript aprovado;
- cobertura real de `93,70%`, reportada de forma arredondada como `94%`;
- Ruff, formatter Ruff, mypy e pre-commit aprovados;
- links Markdown internos versionados validados;
- nenhum código de produção alterado;
- nenhuma regra de negócio ou contrato HTTP alterado.

## O que foi entregue na task 016

- README alinhado ao MVP React e ao CI existentes;
- instruções validadas para instalação local, Docker, migrations e execução;
- usuário de demonstração com imports canônicos e segredos fictícios;
- árvore do repositório, stack, qualidade, fluxo Git e troubleshooting atuais;
- índice técnico e estado arquitetural sincronizados;
- exemplos de CORS alinhados ao frontend React em desenvolvimento.

## Próximo passo obrigatório

1. confirmar worktree limpo e `main` sincronizada;
2. ler `AGENTS.md` e `docs/tasks/017-observability-security.md`;
3. executar o baseline completo;
4. executar somente a task 017.

Não combinar a task 017 com tasks posteriores.

## Restrições de continuidade

- preservar integralmente as regras de negócio registradas em
  `docs/architecture/baseline.md`;
- não alterar contratos HTTP fora dos critérios explícitos da task 017;
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
