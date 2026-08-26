# Checkpoint de continuidade — RailOps

Atualizado em: 26/08/2026

## Estado seguro atual

- branch de continuidade: `main`;
- PR mais recente: [#36 — observabilidade e segurança](https://github.com/ChoqueanoIV/railops-app/pull/36), mesclada;
- merge consolidado na `main`: `77d97e1`;
- nenhuma implementação pendente fora da `main`;
- worktree limpo antes da atualização deste checkpoint documental;
- commit funcional da task 017: `1cd5756`;
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
- 017 — observabilidade, segurança e hardening: integrada no PR #36.

## Validação da task 017

- jobs remotos `Backend` e `Frontend` aprovados no PR;
- 133 testes do backend e 13 testes React aprovados;
- build Vite aprovado;
- ESLint e Prettier aprovados;
- type-check TypeScript aprovado;
- cobertura real de `94,06%`, reportada de forma arredondada como `94%`;
- Ruff, formatter Ruff, mypy e pre-commit aprovados;
- `pip-audit` e `npm audit --omit=dev` sem vulnerabilidades conhecidas;
- nenhuma regra de negócio existente alterada;
- mudanças HTTP e de segurança explicitadas e cobertas por testes.

## O que foi entregue na task 017

- logs JSON com request ID e campos operacionais permitidos;
- headers defensivos e resposta segura para erros inesperados;
- `/health` para liveness e novo `/ready` para prontidão do banco;
- healthchecks Docker alinhados ao readiness;
- JWT sem expiração rejeitado;
- produção exige segredo JWT de 32 bytes e rejeita CORS `*`;
- decisão fundamentada de adiar rate limiting até existir política operacional
  e armazenamento compartilhado.

## Próximo passo obrigatório

1. confirmar worktree limpo e `main` sincronizada;
2. ler `AGENTS.md` e `docs/tasks/018-architecture-decisions.md`;
3. executar o baseline completo;
4. executar somente a task 018.

Não combinar a task 018 com trabalho posterior não planejado.

## Restrições de continuidade

- preservar integralmente as regras de negócio registradas em
  `docs/architecture/baseline.md`;
- não alterar código funcional ao registrar as decisões da task 018;
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
