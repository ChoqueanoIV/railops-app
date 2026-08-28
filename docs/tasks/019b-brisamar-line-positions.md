# Ocupação completa das linhas 22 e 24 do Brisamar

Status: `PLANEJADA`

## Objetivo

Representar integralmente a ocupação operacional das linhas 22 e 24 do Pátio
Brisamar, permitindo registrar simultaneamente as posições superior e inferior
e os travessões associados.

## Dependência

- Task 019 concluída;
- executar antes da Task 019C e das tasks 020–026.

## Regra de negócio aprovada

O formulário deve possuir seis registros independentes:

- L22 Superior;
- L22 Inferior;
- Travessão L22;
- L24 Superior;
- L24 Inferior;
- Travessão L24.

As posições superior e inferior podem conter vagões simultaneamente. Nenhuma
das duas deve excluir ou substituir a outra.

## Escopo

- caracterizar o contrato e a persistência atuais antes da alteração;
- criar migration segura para o novo formato das ocupações;
- preservar a leitura das passagens antigas de L22 e L24;
- atualizar validações, service, repository e schemas necessários;
- atualizar o formulário React e seu carregamento para edição/consulta;
- avaliar e manter compatível o frontend legado enquanto ele existir;
- adicionar testes unitários, de integração, API e frontend;
- validar criação e leitura no Docker com banco migrado.

## Fora do escopo

- implementar rascunho ou confirmação consolidada;
- alterar as demais linhas do Brisamar;
- alterar regras do TECON;
- implementar histórico, filtros ou relatórios;
- apagar ou reescrever migrations já aplicadas.

## Critérios de aceite

- [ ] L22 Superior e L22 Inferior aceitam conteúdos simultâneos;
- [ ] L24 Superior e L24 Inferior aceitam conteúdos simultâneos;
- [ ] Travessão L22 e Travessão L24 possuem campos próprios;
- [ ] criação, consulta e edição carregam os seis valores corretamente;
- [ ] passagens antigas continuam consultáveis sem perda de significado;
- [ ] upgrade e downgrade da migration são testados quando tecnicamente seguros;
- [ ] contratos inválidos continuam retornando erros compatíveis;
- [ ] suítes backend e frontend, lint, tipos e build são aprovados;
- [ ] evidências e checkpoint são atualizados;
- [ ] nenhuma regra fora deste requisito é alterada.

## Risco principal

O modelo atual permite uma única ocupação por linha e guarda `SUP` ou `INF` na
mesma linha. A implementação não pode simplesmente renomear ou apagar esses
registros, pois isso comprometeria passagens existentes. A estratégia de
migration deve ser validada contra dados antigos antes da mudança funcional.

## Evidências

Preencher durante a execução.
