# Estratégia e piloto de deploy

Status: `EM ANDAMENTO`

## Objetivo

Disponibilizar gratuitamente o RailOps para homologação de terceiros, mantendo
o desenvolvimento por branch e PR e sem tratar o piloto como produção.

## Gate aprovado em 03/09/2026

- Cloudflare Pages Free, Render Free e Supabase Free;
- custo máximo de R$ 0, sem cobrança automática;
- URL pública para testadores convidados;
- somente identidades e dados fictícios;
- backup lógico manual antes de mudanças relevantes;
- limitações gratuitas de suspensão, latência e disponibilidade aceitas;
- qualquer uso operacional real depende de novo gate.

## Baseline protegido

- regras de `docs/architecture/baseline.md` e contratos HTTP atuais;
- autenticação JWT, perfis, autorizações e migrations Alembic;
- segredo forte e CORS explícito em `production`;
- nenhum dado cotidiano, URL privada ou credencial versionado.

## Fora de escopo

- produção, dados reais, SLA, backup automático, domínio ou plano pago;
- alteração de regra, contrato, schema ou administração por interface;
- remoção do frontend legado.

## Critérios de aceite

- [x] gate de plataforma, custo, dados, backup e acesso registrado;
- [x] descritores não contêm segredo nem URL privada;
- [x] React possui fallback para rotas diretas;
- [x] API aplica migrations e expõe `/ready`;
- [ ] frontend, API e banco gratuitos provisionados;
- [ ] fluxos críticos aprovados no endereço público com dados fictícios;
- [ ] CORS restrito à origem pública aprovada;
- [ ] checks locais e remotos aprovados;
- [ ] checkpoint registra URLs, limitações e resultado final.

## Evidências parciais

- arquitetura e operação documentadas em `docs/deployment/pilot.md`;
- Blueprint reutiliza a imagem backend, plano Free e variáveis externas;
- migrations ficam no comando de inicialização por limitação do plano gratuito;
- Cloudflare Pages usa o build Vite e fallback explícito de SPA;
- Blueprint parseado com sucesso e confirmado com plano `free`, migrations e
  health check `/ready`;
- 177 testes backend e 28 testes React aprovados;
- Ruff, formatter Ruff, mypy, pre-commit, ESLint, type-check e build Vite
  aprovados;
- artefato Vite contém o fallback `_redirects` esperado;
- PR #48 aberto com `Backend`, `Frontend` e `E2E` aprovados;
- projeto gratuito `railops-piloto` criado no Supabase Free/Nano, na região de
  São Paulo, com Data API desativada e sem inserção de dados reais;
- projeto Supabase anterior preservado; Render e Cloudflare permanecem
  pendentes para a retomada;
- nenhuma regra de negócio, schema ou contrato foi alterado.
