# Consistência do formulário e da revisão da passagem

Status: `CONCLUÍDA`

## Objetivo

Corrigir inconsistências identificadas na homologação humana do formulário e
da revisão consolidada, sem alterar regras ferroviárias, contratos HTTP ou
dados históricos.

## Requisitos aprovados em 06/09/2026

- apresentar valores booleanos como `Sim` ou `Não`, nunca `true` ou `false`;
- quando não houve atendimento no TECON, omitir da revisão os campos que não
  se aplicam;
- deixar explícito que o botão da equipe cria outra linha para outro membro;
- exigir conteúdo em observações e ocorrências quando a respectiva declaração
  de ausência não estiver marcada;
- oferecer as declarações `Sem observações` e `Sem alterações`;
- transformar em maiúsculas os textos operacionais digitados no formulário.

## Decisões de compatibilidade

- as declarações de ausência usam os textos canônicos `SEM OBSERVAÇÕES` e
  `SEM ALTERAÇÕES` no payload já existente;
- nenhum campo, endpoint, schema, migration ou registro histórico foi alterado;
- a validação condicional pertence ao formulário React;
- datas, horários, números, matrícula e opções enumeradas não sofrem conversão
  textual;
- filtros da consulta não fazem parte da passagem final e permaneceram fora do
  escopo.

## Critérios de aceite

- [x] a revisão não exibe booleanos técnicos;
- [x] detalhes não aplicáveis ao TECON ficam ocultos quando não houve atendimento;
- [x] o botão informa que adiciona outro membro à equipe;
- [x] observações e ocorrências são obrigatórias quando as caixas estão desmarcadas;
- [x] marcar a declaração de ausência limpa e desabilita o campo correspondente;
- [x] textos operacionais digitados aparecem em maiúsculas;
- [x] testes automatizados cobrem os comportamentos novos;
- [x] lint, tipagem, testes e build do frontend estão aprovados.

## Evidências

- baseline anterior à alteração foi tentada, mas o `esbuild` teve leitura
  bloqueada pelo redirecionamento do OneDrive dentro do sandbox;
- as validações foram então executadas fora do sandbox, sem modificar o
  ambiente ou arquivos do OneDrive;
- ESLint aprovado;
- TypeScript aprovado;
- 30 testes React aprovados em 6 arquivos;
- build Vite aprovado;
- Prettier aplicado e conferido nos arquivos alterados;
- diff limitado ao formulário, à revisão consolidada, aos testes e à
  documentação desta correção.
