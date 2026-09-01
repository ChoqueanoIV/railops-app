# Testes E2E dos fluxos críticos

Status: `EM ANDAMENTO`

## Objetivo

Automatizar, pelo navegador e contra a aplicação real, os fluxos críticos já
aprovados do RailOps. A task deve detectar regressões entre React, API e
PostgreSQL sem alterar regras de negócio, contratos HTTP ou comportamento das
telas.

## Dependências

- Tasks 019–023 concluídas e integradas;
- frontend React como interface canônica dos fluxos cobertos;
- backend, migrations e PostgreSQL executáveis em ambiente isolado;
- gate da Task 024 aprovado em `docs/ROADMAP.md`.

## Baseline protegido

- primeiro acesso exige matrícula, código de ativação e PIN de quatro dígitos;
- login usa JWT armazenado apenas na sessão do navegador;
- ciclo começa por Brisamar ou TECON e reúne os dois terminais;
- revisão completa antecede a confirmação final;
- confirmação bloqueia novas edições;
- data operacional é a data de início do turno;
- L22 e L24 aceitam SUP, INF e travessão de forma independente;
- Manobrador acessa conteúdo confirmado e PDF individual;
- somente Instrutor e Monitor de Qualidade acessam histórico e consolidados;
- resposta 403 não encerra sessão válida.

## Ferramenta e ambiente aprovados

- Playwright para TypeScript no projeto React;
- Chromium como navegador inicial da suíte;
- execução headless local e na CI de cada PR;
- frontend, backend e PostgreSQL reais em ambiente dedicado ao E2E;
- migrations aplicadas antes da suíte;
- banco separado do ambiente cotidiano e recriado de forma determinística;
- screenshots, vídeos e traces conservados somente em falhas;
- nenhum segredo, token ou credencial real em código ou artefatos.

## Fluxos obrigatórios

### 1. Primeiro acesso e login

- preparar usuário ainda não ativado;
- concluir primeiro acesso com código válido e PIN de quatro dígitos;
- autenticar com o PIN criado;
- alcançar a seleção de terminais;
- confirmar que o token não aparece na URL nem no conteúdo da página.

### 2. Ciclo completo e confirmação

- autenticar um Manobrador preparado pelo ambiente de teste;
- preencher Brisamar, incluindo SUP, INF e travessões de L22/L24;
- preencher TECON no mesmo ciclo;
- revisar os dois terminais na passagem completa;
- confirmar definitivamente;
- recarregar a página e comprovar estado somente leitura;
- comprovar que tentativa de edição posterior permanece bloqueada.

### 3. Consulta e PDF individual

- localizar a passagem confirmada pelos filtros ativos;
- abrir a passagem completa;
- baixar o PDF individual autenticado;
- validar nome, tipo, tamanho mínimo e assinatura `%PDF-`;
- garantir que JWT não seja enviado por query string.

### 4. Permissões de histórico e consolidados

- Manobrador recebe bloqueio ao consultar histórico;
- Manobrador recebe bloqueio ao solicitar PDF/CSV consolidados;
- a sessão do Manobrador permanece válida após 403;
- Instrutor consulta histórico e baixa PDF e CSV consolidados;
- CSV possui cabeçalho esperado e ao menos o ciclo criado pela suíte;
- downloads não contêm nomes de campos de autenticação.

### 5. Recuperação de sessão inválida

- resposta 401 remove a sessão expirada;
- usuário retorna à tela de login;
- nenhuma credencial fica exposta na URL ou em mensagens visíveis.

## Isolamento e dados

- usar IDs determinísticos e matrículas reservadas somente dentro do banco E2E,
  recriado a cada execução;
- nunca reutilizar ou apagar registros do banco cotidiano;
- preparar perfis e códigos de ativação por fixture administrativa restrita ao
  ambiente E2E;
- limpar o banco isolado pela recriação do schema ou volume, não por comandos
  amplos contra ambientes compartilhados;
- congelar ou controlar datas quando necessário para evitar falhas pela janela
  operacional sem enfraquecer a regra de produção;
- permitir paralelismo apenas quando os dados permanecerem independentes.

## Estrutura esperada

```text
frontend/react/
  e2e/
    fixtures/
    primeiro-acesso.spec.ts
    ciclo-confirmacao.spec.ts
    consulta-exportacoes.spec.ts
    permissoes.spec.ts
    sessao.spec.ts
  playwright.config.ts
```

Scripts esperados:

- `npm run test:e2e` para a suíte headless;
- `npm run test:e2e:ui` para diagnóstico local;
- comando de preparação determinística do ambiente documentado;
- job `E2E` separado na CI, sem substituir Backend ou Frontend.

## Evidências e diagnóstico

- relatório HTML do Playwright não deve ser versionado;
- CI pode publicar relatório, screenshot, vídeo e trace quando houver falha;
- logs devem omitir PIN, código de ativação, JWT e strings de conexão;
- seletores devem priorizar papel, rótulo e texto estável, evitando classes CSS;
- esperas devem observar estado visível ou resposta, sem sleeps fixos.

## Fora de escopo

- Firefox, WebKit e dispositivos móveis nesta primeira suíte;
- teste de carga, estresse ou desempenho;
- validação visual por comparação de pixels;
- deploy público ou execução contra produção;
- alterar telas para facilitar testes, salvo atributos acessíveis neutros;
- cobrir todas as combinações de campos já protegidas por testes unitários;
- remover o frontend legado.

## Critérios de aceite

- [ ] cinco fluxos críticos executam contra React, API e PostgreSQL reais;
- [x] banco E2E é isolado e não afeta dados cotidianos;
- [ ] suíte não depende de ordem nem de dados deixados por execução anterior;
- [ ] downloads e permissões são validados pelos perfis aprovados;
- [ ] nenhum token ou segredo aparece em URL, log ou artefato;
- [ ] falhas produzem evidência útil sem persistência em execuções aprovadas;
- [x] `npm run test:e2e` funciona localmente de forma documentada;
- [ ] job E2E passa na CI sem substituir gates existentes;
- [ ] testes backend/frontend atuais permanecem aprovados;
- [ ] documentação e checkpoint registram as evidências finais.

## Evidências

- gate aprovado em 01/09/2026;
- planejamento publicado no commit `fec8534`;
- baseline anterior à implementação: 171 testes backend e 28 testes React;
- Ruff, formatter Ruff, mypy, ESLint, Prettier, type-check e build Vite
  aprovados;
- backend e PostgreSQL locais saudáveis, com `/ready` aprovado;
- `@playwright/test` e Chromium instalados sem vulnerabilidades reportadas pelo
  npm;
- configuração inicial, scripts e exclusão de artefatos adicionados;
- smoke test real no Chromium aprovado ao redirecionar visitante sem sessão
  para o login;
- Vitest e Playwright separados explicitamente para impedir coleta cruzada;
- 28 testes React, smoke E2E, lint, Prettier, type-check, build e auditoria npm
  aprovados após a instalação;
- Compose exclusivo `railops-e2e` aprovado com PostgreSQL em `tmpfs`, API real,
  migrations e desmontagem automática com remoção dos dados temporários;
- fixture determinística protegida por `RAILOPS_ENV=test`, host `db` e banco
  `railops_e2e`; quatro testes impedem execução contra configuração cotidiana;
- ciclo local `npm run test:e2e` aprovado de ponta a ponta: ambiente criado,
  três perfis fictícios preparados, smoke no Chromium aprovado e ambiente
  removido;
- containers cotidianos `railops-app-backend-1` e `railops-app-db-1`
  permaneceram saudáveis e `/ready` respondeu `ok` após o ciclo isolado;
- validação completa após a infraestrutura: 175 testes backend, 28 testes
  React, Ruff, formatter Ruff, mypy, ESLint, Prettier, type-check e build Vite
  aprovados;
- fluxo 1 aprovado no Chromium real: primeiro acesso, definição do PIN, login,
  seleção de terminais e comprovação de que o JWT não aparece na URL nem no
  conteúdo visível;
- suíte E2E com smoke e primeiro acesso: 2 testes aprovados em banco recém-criado
  e descartado ao final;
- nenhum código funcional ou regra de negócio alterado nesta etapa.
