# Listagem e filtros de passagens

Status: `PLANEJADA`

## Objetivo

Implementar uma consulta navegável e paginada dos ciclos confirmados conforme
o contrato aprovado na Task 020. Cada item representa uma passagem completa e
abre Brisamar e TECON juntos em modo somente leitura.

## Dependência

- Task 020 integrada no PR #43;
- contrato em `020-discovery-query-contract.md`.

## Baseline protegido

- endpoints atuais de criação, edição, confirmação e consulta individual;
- identidade do ciclo por data de início do turno, turma e turno;
- confirmação somente com Brisamar e TECON preenchidos;
- bloqueio de edição depois da confirmação;
- regras internas de Brisamar, TECON e janela de turno;
- autenticação JWT atual e acesso por qualquer usuário autenticado;
- registros legados continuam acessíveis pela consulta individual.

## Escopo backend

- criar schemas tipados para filtros, resumo do responsável, item da coleção,
  paginação e resposta da listagem;
- implementar no repository uma consulta somente leitura de ciclos
  `CONFIRMADO`, com contagem total, eager loading e paginação no banco;
- filtrar por intervalo inclusivo da data de início do turno, turma, turno,
  responsável e protocolo;
- interpretar responsável com oito dígitos como matrícula exata e os demais
  textos como trecho do nome, sem diferenciar maiúsculas de minúsculas;
- ordenar por `confirmado_em` decrescente e `id` decrescente;
- calcular os últimos 30 dias no fuso operacional `America/Sao_Paulo` quando o
  período não for informado;
- adicionar ao service um caso de uso de consulta sem mutação ou transação de
  escrita;
- expor `GET /passagens/ciclos` antes da rota dinâmica
  `/passagens/ciclos/{ciclo_id}`;
- exigir autenticação e devolver somente ciclos confirmados;
- reutilizar a montagem dos detalhes consolidados sem expor rascunhos.

## Escopo frontend

- criar a rota protegida `/passagens`;
- adicionar acesso “Consultar passagens” na seleção principal;
- criar formulário com data inicial, data final, turma, turno, responsável e
  protocolo;
- iniciar com o período padrão de 30 dias e 20 itens por página;
- mostrar estados de carregamento, lista vazia e erro recuperável;
- exibir em cada item protocolo, data, turma, turno, responsável e horário da
  confirmação;
- oferecer paginação anterior/próxima com total de itens e páginas;
- abrir o item em `/confirmacao?ciclo=<uuid>`, reutilizando a revisão
  consolidada já existente em modo somente leitura;
- manter layout responsivo e navegação por teclado.

## Contrato de resposta

A implementação deve seguir integralmente o exemplo e as regras definidos em
`020-discovery-query-contract.md`, sem envelope global novo e sem filtro por
terminal.

## Validações e erros

- `pagina` deve ser maior ou igual a 1;
- `por_pagina` deve ficar entre 1 e 100;
- data final não pode ser anterior à data inicial;
- protocolo deve ser UUID válido;
- enums inválidos devem produzir o contrato 422 existente;
- filtros válidos sem correspondência retornam `200` com lista vazia e
  paginação totalizada em zero;
- falha de autenticação preserva o tratamento global atual do React.

## Testes obrigatórios

### Backend

- unitários do service para defaults, intervalo inválido e encaminhamento dos
  filtros;
- integração do repository para estado confirmado, combinações de filtros,
  busca de responsável, ordenação estável, contagem e limites de página;
- API para autenticação, defaults, validação 422 e shape completo da resposta;
- caracterização garantindo que rascunhos nunca aparecem.

### Frontend

- renderização dos resultados e dos metadados;
- aplicação e limpeza de filtros;
- período padrão de 30 dias;
- paginação anterior/próxima;
- estados de carregamento, vazio e erro;
- abertura do detalhe consolidado;
- proteção da nova rota.

## Fora de escopo

- migration ou alteração de tabelas;
- histórico visual dos snapshots;
- perfis/cargos e permissões especiais;
- exportação, impressão, CSV, PDF ou relatórios;
- busca de rascunhos;
- filtro por terminal;
- alteração dos formulários de Brisamar e TECON;
- remoção do frontend legado.

## Critérios de aceite

- [ ] endpoint autenticado retorna somente ciclos confirmados;
- [ ] período padrão, ordenação e paginação seguem a Task 020;
- [ ] todos os filtros aprovados funcionam isolados e combinados;
- [ ] responsável e horário da confirmação aparecem na resposta e na tela;
- [ ] uma linha representa um ciclo completo, sem duplicação por terminal;
- [ ] detalhe reutiliza a revisão consolidada somente leitura;
- [ ] rascunhos e snapshots não são expostos;
- [ ] nenhum schema de banco ou regra operacional é alterado;
- [ ] testes backend e frontend cobrem sucesso, vazio, erro e limites;
- [ ] lint, formatter, type-check, testes e build aprovados;
- [ ] Docker valida migration head existente e fluxo HTTP real;
- [ ] documentação e checkpoint atualizados com evidências.

## Evidências

A preencher durante a execução da task.
