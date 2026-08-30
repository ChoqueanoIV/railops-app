# Ocupação completa das linhas 22 e 24 do Brisamar

Status: `CONCLUÍDA E INTEGRADA NO PR #41`

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

- [x] L22 Superior e L22 Inferior aceitam conteúdos simultâneos;
- [x] L24 Superior e L24 Inferior aceitam conteúdos simultâneos;
- [x] Travessão L22 e Travessão L24 possuem campos próprios;
- [x] criação, consulta e edição carregam os seis valores corretamente;
- [x] passagens antigas continuam consultáveis sem perda de significado;
- [x] upgrade e downgrade da migration são testados quando tecnicamente seguros;
- [x] contratos inválidos continuam retornando erros compatíveis;
- [x] suítes backend e frontend, lint, tipos e build são aprovados;
- [x] evidências e checkpoint são atualizados;
- [x] nenhuma regra fora deste requisito é alterada.

## Risco principal

O modelo atual permite uma única ocupação por linha e guarda `SUP` ou `INF` na
mesma linha. A implementação não pode simplesmente renomear ou apagar esses
registros, pois isso comprometeria passagens existentes. A estratégia de
migration deve ser validada contra dados antigos antes da mudança funcional.

## Evidências

- baseline anterior à alteração: 134 testes de backend e 13 testes React
  aprovados, além de lint, tipos e build;
- migration `e8f1a2b3c4d5` validada no banco Docker preservado com ciclo completo
  de upgrade, downgrade e novo upgrade;
- no upgrade, as ocupações históricas `22 SUP` e `24 INF` conservaram seus
  conteúdos; no downgrade, voltaram ao catálogo anterior com o lado restaurado;
- criação real pela API Docker retornou 12 ocupações e preservou simultaneamente
  `22 SUP`, `22 INF`, `Travessão L22`, `24 SUP`, `24 INF` e `Travessão L24`;
- a passagem histórica `ad1f8db7-a2bb-419b-af7e-8e84319d56ec`, anterior à
  migration, permaneceu consultável com suas oito ocupações originais;
- o registro temporário da validação integrada e todos os seus filhos foram
  removidos em transação; nenhum dado de homologação permaneceu alterado;
- resultado final local: 135 testes de backend e 13 testes React aprovados;
- Ruff, formatter Ruff, mypy, ESLint, Prettier, type-check TypeScript e build
  Vite aprovados;
- frontend React e fallback legado usam os 12 campos independentes, sem o
  seletor exclusivo de posição;
- nenhuma regra do TECON ou das demais linhas do Brisamar foi alterada.
