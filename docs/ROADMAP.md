# Roadmap do produto — fase 2

Status: `PROPOSTO`

Este roadmap começa após a conclusão do pacote técnico das tasks 001–018. A
ordem prioriza validação do produto existente antes de ampliar seu escopo e
preserva as regras registradas em [`architecture/baseline.md`](architecture/baseline.md).

## Estado de partida

O RailOps já possui autenticação, primeiro acesso, seleção de terminal, criação,
consulta por identificador, edição autorizada e confirmação de passagens de
Brisamar e TECON. Backend, frontend, banco, Docker e CI estão automatizados.

Listagem navegável, filtros, consulta visual dos snapshots e exportações em PDF
e CSV já foram implementados. Ainda não existe deploy público.

## Sequência proposta

| ID | Entrega | Dependência | Gate de negócio |
|---|---|---|---|
| 019 | Homologação operacional e de UX | 001–018 | execução por usuários representativos |
| 019B | Ocupação completa de L22/L24 | 019 | regra validada por manobrador |
| 019C | Rascunho e confirmação consolidada | 019B | fluxo e bloqueio final aprovados |
| 020 | Descoberta e contrato de consulta | 019C | público, visibilidade, filtros e paginação |
| 021 | Listagem e filtros de passagens | 020 | contrato aprovado |
| 022 | Histórico auditável de edições | 020, 021 | quem pode consultar e quais dados exibir |
| 023 | Exportações e relatórios | 021, 022 | formato, período, campos e finalidade |
| 024 | Testes E2E dos fluxos críticos | 019–023 | fluxos estáveis para automação |
| 025 | Estratégia e piloto de deploy | 019, 024 | plataforma, custo, dados, backup e acesso |
| 026 | Remoção segura do fallback legado | 019, 024, 025 | React homologado no ambiente alvo |

Os IDs 020–024 estão concluídos. Os IDs 025–026 representam direção planejada,
não autorização para implementar. Cada item deve ganhar uma task detalhada
apenas depois que seu gate for decidido.

## Decisões confirmadas para a Task 020

- consulta por todos os manobradores autenticados, Instrutores e Monitores de
  Qualidade;
- conteúdo confirmado em modo somente leitura;
- filtros por período/data, turma, turno, responsável e protocolo;
- últimos 30 dias por padrão, mais recentes primeiro e 20 itens por página;
- períodos maiores disponíveis sem exclusão dos registros antigos;
- responsável, horário da confirmação e conteúdo final visíveis a todo o
  público autorizado;
- alterações do rascunho visíveis somente a Instrutores e Monitores de
  Qualidade.
- cada item da consulta representa uma passagem completa, reunindo Brisamar e
  TECON; não haverá filtro por terminal, pois todo ciclo confirmado contém os
  dois terminais.

## Decisões ainda pendentes

- política de retenção e tratamento dos dados operacionais;
- ambiente e público do primeiro deploy.

## Decisões confirmadas para a Task 022

- perfis explícitos `MANOBRADOR`, `INSTRUTOR` e `MONITOR_QUALIDADE` associados
  à matrícula cadastrada, sem inferência pelo número;
- usuários existentes permanecem como `MANOBRADOR` por padrão;
- atribuição inicial de Instrutores e Monitores por procedimento administrativo
  seguro no banco, sem criar tela administrativa nesta etapa;
- todos os usuários autenticados continuam consultando o conteúdo final;
- somente Instrutores e Monitores de Qualidade consultam snapshots de edição;
- histórico exibe versão, data/hora, responsável pela alteração e comparação
  entre o estado anterior e o conteúdo final;
- PIN, hashes, tokens, códigos de ativação e demais dados de autenticação nunca
  fazem parte do histórico consultável.

## Decisões confirmadas para a Task 023

- exportações atendem tanto à análise operacional quanto ao arquivamento
  formal;
- CSV consolidado disponível para análise em planilhas;
- PDF individual reúne Brisamar e TECON de uma passagem completa;
- PDF consolidado reúne o período filtrado e apresenta resumo geral;
- Manobrador pode exportar somente o PDF individual das passagens confirmadas
  que já pode consultar;
- Instrutor e Monitor de Qualidade podem exportar PDF individual, PDF
  consolidado e CSV;
- histórico de edições e snapshots não entram nas exportações desta task;
- arquivos incluem dados operacionais finais, nomes e matrículas de responsável
  e equipe;
- PIN, hashes, tokens, códigos de ativação e demais dados de autenticação nunca
  são exportados;
- consolidados reutilizam os filtros atuais, adotam 30 dias por padrão e
  permitem no máximo um ano por arquivo;
- arquivos registram filtros aplicados e data/hora de geração;
- PDF e CSV são gerados sob demanda e entregues ao navegador, sem armazenamento
  no RailOps após o download.

## Decisões confirmadas para a Task 024

- automatizar primeiro acesso/login, ciclo completo, bloqueio após confirmação,
  consulta/downloads, permissões e recuperação de sessão inválida;
- usar Playwright com Chromium como navegador inicial;
- executar React, API e PostgreSQL reais em ambiente E2E isolado;
- executar a suíte localmente e em job próprio na CI de cada PR;
- criar e descartar dados determinísticos sem tocar no banco cotidiano;
- manter screenshots, vídeos e traces somente quando houver falha;
- não alterar regras de negócio nem ampliar o escopo funcional do produto.

## Regra de execução

Executar uma task por branch e PR. Mudança funcional exige critério de aceite,
testes antes e depois e atualização do checkpoint. Nenhuma decisão pendente
deve ser inferida apenas para acelerar a implementação.
