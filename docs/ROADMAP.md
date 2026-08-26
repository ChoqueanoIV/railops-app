# Roadmap do produto — fase 2

Status: `PROPOSTO`

Este roadmap começa após a conclusão do pacote técnico das tasks 001–018. A
ordem prioriza validação do produto existente antes de ampliar seu escopo e
preserva as regras registradas em [`architecture/baseline.md`](architecture/baseline.md).

## Estado de partida

O RailOps já possui autenticação, primeiro acesso, seleção de terminal, criação,
consulta por identificador, edição autorizada e confirmação de passagens de
Brisamar e TECON. Backend, frontend, banco, Docker e CI estão automatizados.

Ainda não existem listagem navegável, filtros, consulta visual dos snapshots de
edição, exportações, relatórios consolidados ou deploy público.

## Sequência proposta

| ID | Entrega | Dependência | Gate de negócio |
|---|---|---|---|
| 019 | Homologação operacional e de UX | 001–018 | execução por usuários representativos |
| 020 | Descoberta e contrato de consulta | 019 | público, visibilidade, filtros e paginação |
| 021 | Listagem e filtros de passagens | 020 | contrato aprovado |
| 022 | Histórico auditável de edições | 020, 021 | quem pode consultar e quais dados exibir |
| 023 | Exportações e relatórios | 021, 022 | formato, período, campos e finalidade |
| 024 | Testes E2E dos fluxos críticos | 019–023 | fluxos estáveis para automação |
| 025 | Estratégia e piloto de deploy | 019, 024 | plataforma, custo, dados, backup e acesso |
| 026 | Remoção segura do fallback legado | 019, 024, 025 | React homologado no ambiente alvo |

Os IDs 020–026 representam direção planejada, não autorização para implementar.
Cada item deve ganhar uma task detalhada apenas depois que seu gate for decidido.

## Decisões pendentes

Antes da Task 020, registrar com os usuários do processo:

- quem pode listar passagens: todos os autenticados, somente a própria turma ou
  outro recorte;
- filtros necessários e período máximo de consulta;
- ordenação e paginação esperadas;
- quem pode visualizar autores e snapshots de alterações;
- quais relatórios são úteis e se a saída deve ser tela, CSV ou PDF;
- política de retenção e tratamento dos dados operacionais;
- ambiente e público do primeiro deploy.

## Regra de execução

Executar uma task por branch e PR. Mudança funcional exige critério de aceite,
testes antes e depois e atualização do checkpoint. Nenhuma decisão pendente
deve ser inferida apenas para acelerar a implementação.
