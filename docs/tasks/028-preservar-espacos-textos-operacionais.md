# Preservação de espaços em textos operacionais

Status: `CONCLUÍDA`

## Objetivo

Permitir a digitação normal de textos com várias palavras nos campos
operacionais que também são convertidos para maiúsculas.

## Causa

Os campos de ocupação das linhas e dos rádios aplicavam `trim()` a cada evento
de digitação. Um espaço digitado no fim do texto era removido imediatamente,
impedindo a entrada da palavra seguinte.

## Correção

- preservar os espaços enquanto o usuário digita;
- continuar convertendo os textos para maiúsculas;
- remover somente espaços externos no momento de montar o payload;
- manter datas, horários e valores booleanos inalterados;
- cobrir descrição da falha do rádio e ocupação da linha em teste automatizado.

## Critérios de aceite

- [x] a descrição da falha aceita frases com espaços;
- [x] o nome do manobrador e o número do rádio preservam a digitação;
- [x] a descrição dos veículos aceita frases com espaços;
- [x] os textos continuam em maiúsculas;
- [x] espaços externos são limpos somente no envio;
- [x] nenhum contrato HTTP, schema, banco ou regra ferroviária é alterado.

## Evidências

- baseline direcionada aprovada com 7 testes antes da alteração;
- suíte React completa aprovada com 30 testes após a alteração;
- casos automatizados confirmam `FALHA NO BOTÃO` e `VAGÕES EM TESTE`;
- ESLint, TypeScript, Prettier e build Vite aprovados;
- diff restrito ao tratamento do estado textual, testes e documentação.
