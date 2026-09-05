# Estratégia e piloto de deploy

Status: `CONCLUÍDA`

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
- [x] React possui fallback nativo do Pages para rotas diretas;
- [x] API aplica migrations e expõe `/ready`;
- [x] frontend, API e banco gratuitos provisionados;
- [x] fluxos críticos aprovados no endereço público com dados fictícios;
- [x] CORS restrito à origem pública aprovada;
- [x] checks locais e remotos aprovados;
- [x] checkpoint registra URLs, limitações e resultado final.

## Evidências parciais

- arquitetura e operação documentadas em `docs/deployment/pilot.md`;
- Blueprint reutiliza a imagem backend, plano Free e variáveis externas;
- migrations ficam no comando de inicialização por limitação do plano gratuito;
- Cloudflare Pages usa o build Vite e o fallback nativo de SPA;
- Blueprint parseado com sucesso e confirmado com plano `free`, migrations e
  health check `/ready`;
- 177 testes backend e 28 testes React aprovados;
- Ruff, formatter Ruff, mypy, pre-commit, ESLint, type-check e build Vite
  aprovados;
- rota pública `/brisamar` aberta diretamente resolveu corretamente para o
  login, confirmando o fallback nativo de SPA;
- PR #48 aberto com `Backend`, `Frontend` e `E2E` aprovados;
- projeto gratuito `railops-piloto` criado no Supabase Free/Nano, na região de
  São Paulo, com Data API desativada e sem inserção de dados reais;
- projeto Supabase anterior preservado; Render e Cloudflare permanecem
  independentes do ambiente cotidiano;
- primeiro deploy Render construiu a imagem, mas falhou com status 127 antes da
  conexão ao banco porque o comando composto foi interpretado como executável;
- inicialização corrigida para script POSIX dedicado, sem alterar aplicação,
  migrations, contratos ou dados;
- API publicada em `https://railops-api-piloto.onrender.com`, com `/health` e
  `/ready` respondendo HTTP 200;
- frontend publicado em `https://railops-piloto.pages.dev`;
- CORS confirmou `https://railops-piloto.pages.dev` como origem exata;
- acesso direto a `/brisamar` resolveu para o login, confirmando o fallback
  nativo do Pages;
- 28 testes React, type-check e build Vite aprovados novamente após o primeiro
  deploy;
- deploy `1e4820d` concluído com sucesso no Pages sem aviso de redirecionamento,
  seguido de nova validação pública de `/brisamar`;
- nenhuma regra de negócio, schema ou contrato foi alterado.
- quatro identidades exclusivamente fictícias foram cadastradas e ativadas no
  banco do piloto, cobrindo primeiro acesso, Manobrador, Instrutor e Monitor de
  Qualidade, sem versionar credenciais;
- o plano gratuito do Render apresentou a suspensão esperada; após o despertar
  da API, o primeiro acesso foi concluído sem escrita parcial;
- login público de Manobrador e ciclo completo Brisamar + TECON aprovados, com
  revisão consolidada, correção anterior à confirmação e bloqueio posterior;
- L22 e L24 foram validadas com ocupações simultâneas superior e inferior e com
  seus respectivos travessões;
- tentativa de edição pela URL direta após a confirmação foi bloqueada pela
  aplicação;
- PDF individual retornou HTTP 200 para Manobrador; histórico e CSV consolidado
  retornaram HTTP 403 para esse perfil, preservando as autorizações;
- histórico e CSV consolidado retornaram HTTP 200 para Instrutor e Monitor de
  Qualidade;
- toda a homologação pública utilizou nomes, observações, códigos e composições
  fictícios, sem dados cotidianos.

## Encerramento

- PR #48 integrado à `main` no merge `ebc15b2`;
- branches de produção do Cloudflare Pages e do Blueprint Render alteradas para
  `main`, mantendo os deploys automáticos;
- validação posterior confirmou `/ready` em HTTP 200, CORS restrito à origem
  pública e as rotas `/login` e `/brisamar` em HTTP 200;
- o piloto permanece gratuito, sujeito a suspensão, latência e disponibilidade
  dos planos Free e inadequado para uso operacional real.
