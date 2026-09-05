# Checkpoint de continuidade — RailOps

Atualizado em: 05/09/2026

## Estado seguro atual

- branch de continuidade: `main`;
- PR mais recente: [#48 — piloto gratuito de deploy](https://github.com/ChoqueanoIV/railops-app/pull/48), mesclada;
- merge consolidado na `main`: `ebc15b2`;
- Task 019B concluída, validada e integrada;
- Task 019C concluída, validada e integrada;
- Task 020 concluída, validada e integrada;
- Task 021 concluída, validada e integrada;
- Task 022 concluída, validada e integrada;
- Task 023 concluída, validada e integrada;
- Task 024 concluída e integrada: cinco fluxos críticos aprovados localmente e
  no job E2E remoto do PR #47;
- Task 025 concluída e integrada, com infraestrutura gratuita publicada,
  homologação pública aprovada e provedores acompanhando a branch `main`;
- piloto publicado em Cloudflare Pages, Render Free e Supabase Free, somente
  com identidades e dados fictícios;
- homologação pública aprovada com Manobrador, Instrutor e Monitor de Qualidade,
  incluindo primeiro acesso, ciclo completo, confirmação, bloqueio de edição,
  PDF, histórico e CSV conforme as permissões vigentes;
- baseline da Task 023 preservado; validação atual com 177 testes backend, 28
  testes React e smoke real no Chromium;
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
- 019B — ocupação completa de L22/L24: integrada no PR #41.
- 019C — rascunho e confirmação consolidada: integrada no PR #42.
- 020 — descoberta e contrato de consulta: integrada no PR #43.
- 021 — listagem e filtros de passagens: integrada no PR #44.
- 022 — histórico auditável de edições: integrada no PR #45.
- 023 — exportações e relatórios: integrada no PR #46.

O pacote técnico das tasks 001–018 foi integralmente executado. A Task 019 foi
concluída e originou as correções 019B e 019C. Ambas estão integradas na
`main`.

## Validação da task 025

- frontend público em `https://railops-piloto.pages.dev` e API pública em
  `https://railops-api-piloto.onrender.com`;
- Cloudflare Pages, Render e Supabase mantidos nos planos gratuitos;
- quatro identidades fictícias ativadas para cobrir primeiro acesso e os três
  perfis, sem credenciais versionadas;
- ciclo completo Brisamar + TECON aprovado, incluindo L22/L24 simultâneas,
  travessões, revisão, correção, confirmação e bloqueio posterior de edição;
- PDF individual aprovado para Manobrador; histórico e CSV retornaram 403 para
  esse perfil e 200 para Instrutor e Monitor de Qualidade;
- suspensão e atraso de partida do Render Free observados e aceitos; a retomada
  não produziu escrita parcial;
- PR #48 aprovado nos jobs Backend, Frontend, E2E e Cloudflare Pages e integrado
  no merge `ebc15b2`;
- Cloudflare Pages e Blueprint Render configurados para acompanhar `main`;
- validação pós-migração aprovou `/ready`, CORS e rotas diretas públicas;
- nenhuma regra de negócio, schema ou contrato HTTP foi alterado.

## Validação da task 024

- Playwright e Chromium configurados no frontend React;
- Compose `railops-e2e` independente, com banco temporário em `tmpfs`, API real
  e migrations;
- fixture determinística cria usuários Manobrador, Instrutor e de primeiro
  acesso somente após validar ambiente, host e nome do banco E2E;
- quatro testes unitários protegem o seed contra configurações cotidianas;
- `npm run test:e2e` cria o ambiente, prepara os dados, executa o Chromium e
  remove containers, rede e dados temporários automaticamente;
- smoke real aprovado contra React, API e PostgreSQL isolados;
- primeiro acesso e login reais aprovados, incluindo seleção de terminais e
  ausência do JWT na URL e no conteúdo visível;
- ciclo Brisamar + TECON aprovado com revisão, confirmação, recarga somente
  leitura e bloqueio de tentativa posterior de edição;
- teste E2E encontrou e protegeu a correção do vazamento de estado do formulário
  Brisamar ao navegar para TECON;
- consulta filtrada e PDF individual aprovados, incluindo nome, MIME, tamanho,
  assinatura `%PDF-` e ausência do JWT na URL;
- `Content-Disposition` exposto pelo CORS para preservar no navegador o nome
  definido pela API;
- permissões reais aprovadas: Manobrador bloqueado por 403 sem logout e
  Instrutor autorizado no histórico e nos consolidados CSV/PDF;
- CSV/PDF consolidados validados sem nomes de campos de autenticação;
- suíte E2E atual com 5 testes aprovados em paralelo e sem dependência de ordem;
- recuperação de sessão inválida aprovada com 401 real, limpeza do JWT e retorno
  seguro ao login;
- suíte funcional completa com 6 testes E2E paralelos;
- job `E2E` separado configurado na CI, preservando `Backend` e `Frontend` e
  publicando artefatos somente em falhas;
- PR #47 com `Backend`, `Frontend` e `E2E` aprovados e integrado à `main` no
  merge `1b88fb1`;
- ambiente cotidiano permaneceu saudável e `/ready` respondeu `ok` após o
  ciclo;
- 177 testes backend e 28 testes React aprovados;
- Ruff, formatter Ruff, mypy, ESLint, Prettier, type-check e build Vite
  aprovados;
- nenhum contrato HTTP, comportamento de tela ou regra de negócio foi alterado.

## Validação da task 023

- PDF individual disponível a qualquer usuário autenticado para ciclos
  confirmados, reunindo Brisamar e TECON;
- PDF e CSV consolidados restritos a Instrutor e Monitor de Qualidade;
- filtros existentes reutilizados, período padrão de 30 dias e limite máximo
  de um ano por arquivo;
- CSV UTF-8 com uma linha por ciclo, listas determinísticas e proteção contra
  fórmulas de planilha;
- arquivos gerados em memória e entregues como download, sem persistência no
  servidor e sem snapshots ou credenciais;
- interface React com downloads autenticados, carregamento, erros e preservação
  da sessão em resposta 403;
- 171 testes backend e 28 testes React aprovados;
- Ruff, formatter Ruff, mypy, ESLint, Prettier, type-check e build Vite
  aprovados;
- PDFs individual e consolidado inspecionados visualmente, inclusive com
  paginação multipágina;
- imagem Docker reconstruída, backend saudável e `/ready` aprovado sem alterar
  o volume PostgreSQL;
- homologação HTTP real aprovou 403 para Manobrador e 200 em CSV/PDF para
  Instrutor; usuários temporários foram removidos pelos UUIDs criados;
- banco local sem ciclo confirmado para homologação HTTP individual; cenário
  coberto por testes automatizados e inspeção visual;
- jobs remotos `Backend` e `Frontend` aprovados no PR #46;
- commit funcional: `34b3b31`.
- merge `a8cab9d` integrado na `main` sem conflitos.

## Validação da task 022

- perfis explícitos persistidos com `MANOBRADOR` como padrão seguro;
- endpoint paginado de histórico restrito a Instrutor e Monitor de Qualidade;
- comparação legível entre cada snapshot anterior e o conteúdo final;
- resposta 403 preserva a sessão autenticada do Manobrador;
- 156 testes backend e 23 testes React aprovados;
- histórico vazio, recurso inexistente, múltiplas versões, ordenação e
  paginação cobertos por testes automatizados;
- Ruff, mypy, ESLint, Prettier, type-check e build Vite aprovados;
- migration `a2b3c4d5e6f7` aprovada em PostgreSQL real com upgrade, downgrade e
  novo upgrade, preservando usuário e aplicando o perfil padrão;
- banco temporário de validação removido e banco persistente não alterado;
- HTTP real isolado aprovado para os três perfis: Manobrador acessa o conteúdo
  final e recebe 403 no histórico; Instrutor e Monitor recebem 200 no histórico;
- resposta real contém versão e autor, sem campos de autenticação;
- contêiner e banco temporários da homologação HTTP removidos ao final;
- procedimento administrativo idempotente de atribuição de perfil documentado;
- nenhuma regra operacional de Brisamar, TECON, turno, edição ou confirmação
  foi modificada.
- jobs remotos `Backend` e `Frontend` aprovados no PR #45;
- merge `0d30b51` integrado na `main` sem conflitos.

## Validação da task 019C

- 144 testes backend e 14 testes React aprovados;
- Ruff, formatter Ruff, mypy, ESLint, Prettier e type-check aprovados;
- build Vite de produção aprovado;
- migration `f9a2b3c4d5e6` validada com upgrade, downgrade e novo upgrade;
- seis passagens históricas preservadas sem associação retroativa inventada;
- fluxo Docker completo aprovado, incluindo retomada, revisão, correção,
  confirmação idempotente e bloqueio posterior;
- dados temporários da homologação removidos em transação;
- nenhuma regra interna de Brisamar, TECON ou janela de turno foi alterada.
- jobs remotos `Backend` e `Frontend` aprovados no PR #42;
- merge `02e9683` integrado na `main` sem conflitos.

## Validação da task 019B

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
- jobs remotos `Backend` e `Frontend` aprovados no PR #41;
- merge `cfaa59d` integrado na `main` sem conflitos.

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

1. manter o piloto restrito a testadores convidados e dados fictícios;
2. coletar feedback sem alterar regras de negócio implicitamente;
3. retomar a Task 026 pela baseline de testes antes de remover o frontend
   estático legado;
4. preservar integralmente regras, contratos e dados cotidianos.

O gate da Task 026 foi aprovado em 05/09/2026. A baseline local principal foi
aprovada e o frontend estático autorizado foi removido; a validação posterior e
o PR ainda estão pendentes.

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
$env:PYTHONPATH=(Resolve-Path '.venv/Lib/site-packages').Path
& 'C:\Users\Leandro CHOQUE\AppData\Local\Programs\Python\Python313\python.exe' -m pytest
```

Para uma reconstrução limpa, o fluxo preferencial está documentado em
`docs/README.md` e usa `uv sync --frozen`.
