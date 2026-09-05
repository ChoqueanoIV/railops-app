# Remoção segura do frontend legado

Status: `CONCLUÍDA`

## Objetivo

Remover somente a implementação antiga em HTML, CSS e JavaScript após a
homologação do React no ambiente público, sem alterar regras de negócio,
contratos HTTP, compatibilidades históricas ou comportamento observável.

## Gate aprovado em 05/09/2026

- React homologado localmente, no E2E, na CI e no piloto público;
- remoção limitada aos arquivos estáticos anteriores ao React;
- compatibilidades da API, adaptadores internos, migrations, schema e registros
  históricos permanecem fora do escopo;
- testes obrigatoriamente executados antes e depois da remoção;
- validação pública posterior obrigatória;
- execução em branch e PR próprios.

## Baseline protegido

- todos os fluxos e autorizações registrados nas Tasks 019–025;
- rotas React `/login`, `/terminal`, `/brisamar`, `/tecon`, `/confirmacao`,
  `/passagens` e consulta de histórico;
- contratos de sucesso e erro da API, inclusive o campo compatível `detail`;
- adaptadores de importação internos do backend;
- campos e registros históricos marcados como legados no banco;
- deploy gratuito acompanhando a branch `main`.

## Escopo de remoção

- `frontend/index.html`;
- `frontend/terminal.html`;
- `frontend/brisamar.html`;
- `frontend/tecon.html`;
- `frontend/confirmacao.html`;
- `frontend/js/`;
- `frontend/css/styles.css`;
- referências documentais que afirmem que esses arquivos continuam disponíveis.

## Fora de escopo

- qualquer arquivo em `frontend/react/`;
- `backend/app/api/errors.py` e compatibilidade do envelope HTTP;
- routers e models mantidos para compatibilidade interna ou histórica;
- migrations, schema e transformação de dados existentes;
- alteração visual ou funcional do React;
- alteração de infraestrutura, credenciais ou dados do piloto.

## Sequência obrigatória

1. executar e registrar a baseline completa;
2. confirmar que nenhum processo de build, teste ou deploy usa os estáticos;
3. remover apenas os arquivos aprovados;
4. atualizar documentação e inventário arquitetural;
5. repetir todos os checks locais relevantes;
6. abrir PR e exigir Backend, Frontend, E2E e Cloudflare Pages aprovados;
7. validar as rotas públicas após o merge e atualizar o checkpoint.

## Critérios de aceite

- [x] baseline anterior registrada e aprovada;
- [x] somente o frontend estático antigo foi removido;
- [x] React permanece com todas as rotas e fluxos homologados;
- [x] nenhuma compatibilidade de API, banco ou histórico foi removida;
- [x] backend, frontend, E2E, lint, tipos e build permanecem aprovados;
- [x] deploy público permanece saudável após a integração;
- [x] documentação e checkpoint refletem o estado final;
- [x] nenhuma regra de negócio, schema ou contrato HTTP foi alterado.

## Evidências

- gate aprovado pelo responsável do produto em 05/09/2026;
- inventário confirmou cinco HTML, cinco JavaScript e um CSS fora do React;
- busca estática não encontrou montagem ou entrega desses arquivos pelo backend;
- Cloudflare Pages publica exclusivamente `frontend/react/dist`;
- execução pausada antes da baseline de testes para avaliação do orçamento de
  uso disponível.
- baseline local aprovada com 177 testes backend, 28 testes React, Ruff,
  formatter Ruff, mypy, ESLint, Prettier, TypeScript e build Vite;
- baseline E2E local bloqueada antes de iniciar porque o Docker Desktop 4.87
  encontrou um socket temporário travado; a baseline remota do PR #49, sobre a
  mesma `main`, foi aprovada;
- nenhuma imagem, volume ou configuração do Docker foi redefinida para contornar
  o bloqueio ambiental;
- cinco HTML, cinco JavaScript e um CSS removidos; React, backend, migrations e
  compatibilidades históricas permaneceram intactos.
- validação local posterior aprovada com 177 testes backend, 28 testes React,
  Ruff, formatter Ruff, mypy, ESLint, Prettier, TypeScript e build Vite;
- busca estrutural posterior encontrou referências aos caminhos removidos
  somente no inventário desta task, sem consumidor ativo.
- PR #50 aprovado nos jobs Backend, Frontend, E2E e Cloudflare Pages; o E2E
  remoto executou os fluxos reais contra React, API e PostgreSQL isolados.
- PR #50 integrado à `main` no merge `e6b5400`;
- checks da própria `main` aprovados, incluindo o E2E posterior ao merge;
- piloto público aprovado após a integração: `/ready`, CORS, `/login` e rota
  direta `/brisamar` responderam corretamente.
