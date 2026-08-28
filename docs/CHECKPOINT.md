# Checkpoint de continuidade — RailOps

Atualizado em: 28/08/2026

## Estado seguro atual

- branch de trabalho atual: `feat/brisamar-l22-l24-completas`;
- PR mais recente: [#40 — homologação operacional da Task 019](https://github.com/ChoqueanoIV/railops-app/pull/40), mesclada;
- merge consolidado na `main`: `34e8cc6`;
- Task 019B concluída e validada localmente, aguardando commit e integração;
- Task 019C permanece como próximo requisito, sem implementação iniciada;
- commit do roadmap da fase 2: `9082444`;
- commits da task 018: `89d4048` e `b3216dd`;
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
- 018 — ADRs e governança arquitetural: integrada no PR #37.
- 019A — serialização dos erros de validação 422: integrada no PR #39.

O pacote técnico das tasks 001–018 foi integralmente executado. A Task 019 foi
concluída e originou as correções 019B e 019C. A 019B está concluída e validada
localmente; a 019C ainda não foi iniciada.

## Validação local da task 019B

- 135 testes do backend e 13 testes React aprovados;
- Ruff, formatter Ruff, mypy, ESLint, Prettier e type-check aprovados;
- build Vite de produção aprovado;
- migration `e8f1a2b3c4d5` validada com upgrade, downgrade e novo upgrade no
  banco Docker preservado;
- dados históricos de L22/L24 preservados e consultáveis;
- criação real pela API confirmou os 12 campos independentes, inclusive lados
  superior e inferior simultâneos e os travessões L22/L24;
- registro temporário usado no teste integrado removido em transação;
- nenhuma regra do TECON ou das demais linhas foi alterada.

## Validação da task 019A

- jobs remotos `Backend` e `Frontend` aprovados no PR;
- 134 testes do backend aprovados, com cobertura mantida em `94%`;
- Ruff, formatter Ruff, mypy e pre-commit aprovados;
- cenário real reproduzido no Docker e corrigido de HTTP 500 para HTTP 422;
- contrato legado em `detail` e código `REQUEST_VALIDATION_ERROR` preservados;
- nenhuma regra de negócio alterada.

## Validação da task 018

- jobs remotos `Backend` e `Frontend` aprovados no PR;
- 133 testes do backend e 13 testes React aprovados;
- build Vite aprovado;
- ESLint e Prettier aprovados;
- type-check TypeScript aprovado;
- cobertura real de `94,06%`, reportada de forma arredondada como `94%`;
- Ruff, formatter Ruff, mypy e pre-commit aprovados;
- nenhuma regra de negócio existente alterada;
- oito ADRs com contexto, decisão, alternativas e consequências;
- links internos da documentação validados.

## O que foi entregue na task 018

- decisões arquiteturais vigentes registradas em oito ADRs;
- índice e regras de governança para decisões futuras;
- decisões explícitas sobre evolução incremental, compatibilidade da API, `uv`,
  transações, ORM, React/Vite, token no navegador e Docker local;
- navegação da documentação e evidências da task atualizadas;
- nenhum código funcional alterado.

## Próximo passo obrigatório

1. revisar o diff final da Task 019B, criar o commit e publicar a branch;
2. abrir e validar o PR da 019B, aguardando os checks remotos;
3. integrar a 019B antes de iniciar a 019C;
4. executar somente `docs/tasks/019c-consolidated-draft-confirmation.md` após
   a integração da 019B;
5. não iniciar as tasks 020–026 antes da conclusão da 019C.

Não implementar os itens 020–026 antes da homologação e da aprovação de seus
gates de negócio.

## Restrições de continuidade

- preservar integralmente as regras de negócio registradas em
  `docs/architecture/baseline.md`;
- não alterar regras de negócio sem requisito e aceite explícitos;
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
