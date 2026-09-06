# Linhas livres e layout dos registros do turno

Status: `CONCLUÍDA`

## Objetivo

Tornar explícita a situação de todas as linhas dos dois terminais e melhorar a
organização visual das declarações de ausência dos registros do turno.

## Requisitos aprovados em 06/09/2026

- cada linha do Brisamar e do TECON possui a opção `Livre`;
- sem essa opção marcada, a descrição de veículos ou situação é obrigatória;
- ao marcar `Livre`, o campo textual da linha é limpo e desabilitado;
- o payload continua usando o campo existente `veiculos`, com o valor canônico
  `LIVRE`, sem alterar o contrato HTTP;
- `Sem observações` fica ao lado do título `Observações`;
- `Sem alterações` fica ao lado do título `Relatório de ocorrências`;
- o layout permanece responsivo em telas menores.

## Critérios de aceite

- [x] todas as linhas de ambos os terminais exigem descrição ou `Livre`;
- [x] o estado `Livre` é apresentado e enviado sem novo campo de API;
- [x] as declarações de ausência aparecem junto aos respectivos títulos;
- [x] os campos continuam acessíveis por seus rótulos;
- [x] testes unitários cobrem a obrigatoriedade condicional;
- [x] o E2E preenche ocupações e marca as linhas restantes como livres;
- [x] nenhuma migration, schema ou regra ferroviária não solicitada é alterada.

## Evidências

- baseline direcionada aprovada com 7 testes antes da alteração;
- suíte React aprovada com 31 testes após a alteração;
- novo teste cobre linha obrigatória, marcação `Livre`, bloqueio e reabertura;
- roteiro E2E atualizado para declarar todas as linhas vazias como livres;
- ESLint, TypeScript, Prettier e build Vite aprovados;
- alteração restrita ao formulário React, estilos, testes e documentação.
