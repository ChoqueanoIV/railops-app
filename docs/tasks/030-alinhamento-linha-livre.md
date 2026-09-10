# Alinhamento visual da opção de linha livre

Status: `CONCLUÍDA`

## Objetivo

Corrigir o espaçamento da opção `Livre` na ocupação das linhas em telas de
computador e celular, sem alterar a regra ou o payload implementados na Task
029.

## Causa

O seletor CSS que aplicava largura total ao campo de ocupação também atingia o
checkbox dentro da mesma linha. O quadrado ocupava toda a coluna e separava-se
visualmente do texto `Livre`.

## Correção

- aplicar largura total somente ao campo textual que é filho direto da linha;
- manter checkbox e texto como um conjunto compacto no computador;
- no celular, apresentar o código da linha e a opção `Livre` no cabeçalho da
  linha, com o campo textual ocupando toda a largura logo abaixo;
- preservar acessibilidade, obrigatoriedade e valor canônico `LIVRE`.

## Critérios de aceite

- [x] checkbox e texto `Livre` permanecem juntos;
- [x] alinhamento funciona em telas largas;
- [x] layout móvel não cria separação horizontal indevida;
- [x] campo de ocupação mantém largura integral;
- [x] nenhuma regra de negócio ou contrato HTTP é alterado.

## Evidências

- baseline direcionada aprovada com 8 testes antes da alteração;
- suíte React completa aprovada com 31 testes após a alteração;
- ESLint, TypeScript, Prettier e build Vite aprovados;
- diff funcional restrito ao CSS responsivo;
- arquivos da apresentação em `entregas/` permaneceram fora desta task.
