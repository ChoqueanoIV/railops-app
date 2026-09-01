# Exportações e relatórios

Status: `CONCLUÍDA E INTEGRADA`

## Objetivo

Gerar arquivos sob demanda para análise operacional e arquivamento formal das
passagens confirmadas, preservando integralmente as permissões, os filtros e o
conteúdo final já aprovados.

## Dependências

- Task 021 integrada no PR #44;
- Task 022 integrada no PR #45;
- gate de formato, período, campos e finalidade aprovado em
  `docs/ROADMAP.md`.

## Baseline protegido

- ciclo confirmado reúne Brisamar e TECON em uma passagem completa;
- conteúdo final permanece disponível a todos os usuários autenticados;
- snapshots são restritos a Instrutor e Monitor de Qualidade;
- filtros atuais usam data de início, turma, turno, responsável e protocolo;
- período padrão de 30 dias e ordenação mais recente primeiro;
- nenhuma regra de preenchimento, edição ou confirmação pode ser alterada;
- dados de autenticação nunca fazem parte de respostas operacionais.

## Entregas aprovadas

### PDF individual

- uma passagem completa por arquivo, reunindo Brisamar e TECON;
- disponível a qualquer usuário autenticado que possa consultar a passagem;
- inclui protocolo, data, turma, turno, responsável, confirmação, equipe,
  ocupações, rádios, ocorrências, observações e detalhes dos dois terminais;
- permanece somente leitura e não inclui snapshots de edição.

### PDF consolidado

- disponível somente a Instrutor e Monitor de Qualidade;
- reúne as passagens confirmadas correspondentes aos filtros aplicados;
- apresenta filtros, data/hora da geração, total e resumo operacional do
  período;
- identifica cada passagem por protocolo, data, turma, turno, responsável,
  confirmação, ocorrências e resumo dos terminais.

### CSV consolidado

- disponível somente a Instrutor e Monitor de Qualidade;
- uma linha por ciclo confirmado completo;
- colunas estáveis e documentadas para filtros, metadados, responsável, equipe,
  ocorrências e dados finais de Brisamar e TECON;
- codificação UTF-8 compatível com planilhas, preservando acentos;
- listas internas devem usar representação determinística e documentada, sem
  criar linhas que dupliquem o mesmo ciclo.

## Período e filtros

- reutilizar `data_inicio`, `data_fim`, `turma`, `turno`, `responsavel` e
  `protocolo` da Task 021;
- aplicar os últimos 30 dias quando o período não for informado;
- aceitar intervalo inclusivo máximo de um ano;
- orientar divisão em arquivos separados quando o período solicitado exceder
  esse limite;
- exportar todos os itens correspondentes, sem depender da página visível;
- preservar a ordenação por confirmação e protocolo usada na consulta.

## Contrato HTTP proposto

- `GET /passagens/ciclos/{ciclo_id}/exportacao.pdf` para PDF individual;
- `GET /passagens/ciclos/exportacoes.pdf` para PDF consolidado;
- `GET /passagens/ciclos/exportacoes.csv` para CSV consolidado;
- autenticação Bearer obrigatória em todas as rotas;
- autorização especial reutiliza a dependência aprovada na Task 022;
- respostas usam `Content-Disposition: attachment` com nome previsível;
- arquivos são transmitidos diretamente e não persistidos no servidor;
- intervalo superior a um ano retorna erro padronizado sem gerar arquivo;
- recurso inexistente ou não confirmado não produz PDF individual.

## Segurança e privacidade

- permitir PDF individual a Manobrador, Instrutor e Monitor de Qualidade;
- restringir consolidados a Instrutor e Monitor de Qualidade;
- incluir nomes e matrículas operacionais aprovados;
- excluir perfil interno, senha, PIN, hashes, JWT, código de ativação e qualquer
  outra credencial;
- excluir snapshots e histórico de edições;
- não registrar conteúdo completo dos arquivos em logs;
- não armazenar arquivos, caminhos ou cópias temporárias permanentes.

## Escopo backend

- separar coleta tipada de dados, representação tabular e renderização;
- reutilizar repository e filtros existentes sem duplicar regras de consulta;
- processar todos os resultados do período com limite explícito e uso de memória
  controlado;
- produzir CSV determinístico e protegido contra interpretação de fórmulas;
- produzir PDF legível, paginado e com cabeçalho/rodapé RailOps;
- testar cabeçalhos HTTP, nomes dos arquivos, conteúdo e permissões;
- manter os endpoints JSON atuais inalterados.

## Escopo frontend

- adicionar “Baixar PDF” no detalhe da passagem completa;
- adicionar “Exportar CSV” e “Exportar PDF” na listagem filtrada;
- preservar os filtros ativos na solicitação consolidada;
- apresentar claramente erro de permissão e intervalo superior a um ano;
- iniciar download autenticado sem expor JWT na URL;
- manter estados de carregamento e evitar solicitações duplicadas.

## Testes obrigatórios

### Backend

- autorização dos três perfis em cada formato;
- passagem inexistente, rascunho e ciclo confirmado;
- período padrão, limite de um ano e filtros combinados;
- CSV com uma linha por ciclo, acentos, listas e proteção contra fórmulas;
- PDF individual e consolidado com conteúdo e paginação mínimos;
- ausência de snapshots e credenciais nos arquivos;
- cabeçalhos de download e nomes determinísticos;
- compatibilidade dos endpoints existentes.

### Frontend

- download individual disponível aos três perfis;
- consolidados aprovados e bloqueados conforme perfil;
- filtros encaminhados integralmente;
- resposta binária baixada sem inserir token na URL;
- estados de carregamento, erro e nova tentativa;
- sessão válida preservada em resposta 403.

## Fora de escopo

- exportar histórico de edições;
- armazenar, agendar ou enviar arquivos por e-mail;
- dashboard analítico ou gráficos;
- XLSX ou integração direta com planilhas externas;
- assinatura digital ou valor jurídico do PDF;
- política geral de retenção dos registros operacionais;
- alteração de perfis pela interface;
- deploy público.

## Critérios de aceite

- [x] PDF individual reúne Brisamar e TECON e respeita acesso autenticado;
- [x] PDF e CSV consolidados são restritos aos perfis especiais;
- [x] filtros e período máximo de um ano são aplicados corretamente;
- [x] uma linha CSV representa um ciclo completo sem duplicação;
- [x] nomes e matrículas operacionais aparecem conforme aprovado;
- [x] snapshots e dados de autenticação não aparecem nos arquivos;
- [x] arquivos são gerados sob demanda e não persistidos;
- [x] downloads autenticados funcionam na interface React;
- [x] endpoints existentes e regras operacionais permanecem inalterados;
- [x] backend, frontend, Docker e CI são aprovados;
- [x] documentação e checkpoint registram as evidências finais.

## Evidências

- baseline anterior à implementação: 156 testes backend e 23 testes React;
- Ruff, formatter Ruff, mypy, ESLint, Prettier e type-check aprovados;
- build Vite de produção aprovado;
- branch funcional criada a partir da `main` limpa após a integração da Task
  022;
- nenhum código funcional ou schema de banco alterado nesta etapa.
- backend parcial implementado: PDF individual, PDF consolidado e CSV
  consolidado gerados sob demanda;
- consolidados protegidos por perfil especial, período padrão de 30 dias e
  intervalo máximo de um ano;
- CSV validado com uma linha por ciclo, UTF-8 com BOM, listas determinísticas e
  proteção contra fórmulas de planilha;
- PDF individual e consolidado validados visualmente, inclusive paginação;
- 171 testes backend, Ruff, formatter Ruff e mypy aprovados após esta etapa.
- frontend React conectado aos três downloads com token somente no cabeçalho,
  filtros ativos, carregamento, erro e preservação da sessão em resposta 403;
- 28 testes React, ESLint, Prettier, type-check e build Vite aprovados.
- imagem Docker reconstruída com `reportlab`, backend saudável e endpoint
  `/ready` aprovado sem alterar o volume PostgreSQL;
- homologação HTTP real: Manobrador recebeu 403 nos consolidados e Instrutor
  recebeu 200 no CSV e no PDF, com tipos de conteúdo corretos;
- usuários aleatórios da homologação removidos pelos UUIDs criados; o banco
  local não continha ciclo confirmado para repetir o PDF individual via HTTP;
  esse cenário permanece coberto pelos testes automatizados e pela inspeção
  visual do PDF com ciclo completo;
- jobs remotos `Backend` e `Frontend` aprovados no PR #46.
- PR #46 mesclado na `main` pelo merge `a8cab9d`.
