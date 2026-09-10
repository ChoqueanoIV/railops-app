# Task 034 — Revisão operacional e orientação do fluxo

## Objetivo

Melhorar a leitura da revisão consolidada e indicar corretamente o destino do
botão final de cada terminal, sem alterar o funcionamento do ciclo.

## Comportamento preservado

- o primeiro terminal pode ser Brisamar ou TECON;
- ao salvar o primeiro terminal, a API informa o terminal pendente e o sistema
  abre seu formulário;
- ao salvar o segundo terminal, o sistema abre a revisão consolidada;
- confirmação final e bloqueio de edição permanecem inalterados.

## Alterações

- rótulos e valores da revisão passam a ocupar a mesma linha em uma grade;
- equipe, linhas, registros e dados específicos recebem hierarquia visual;
- campos técnicos dos detalhes recebem nomes públicos amigáveis;
- sem ciclo em andamento, o botão informa “Avançar para o próximo terminal”;
- com o outro terminal já preenchido, informa “Avançar para revisão”.

## Critérios de aceite

- a ordem de início dos terminais não afeta o texto nem o destino correto;
- nenhuma informação operacional é omitida ou transformada;
- a revisão permanece legível em computador e celular;
- testes de componente e E2E caracterizam os dois destinos;
- checks do frontend e pipeline passam.

## Evidências

Executadas em 10/09/2026:

- Vitest: 35 testes aprovados;
- ESLint: aprovado;
- TypeScript: aprovado;
- Prettier: aprovado;
- build Vite: aprovado;
- E2E atualizado para validar separadamente o primeiro e o segundo terminal;
- API, banco, payloads e regras de confirmação: não alterados.
