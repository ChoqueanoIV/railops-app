# Preenchimento obrigatório sem valores indefinidos

Status: `CONCLUÍDA`

## Objetivo

Impedir que uma passagem nova seja salva com informações operacionais em
branco e eliminar a apresentação de `Não informado` na revisão consolidada.

## Requisitos aprovados em 10/09/2026

- todo conteúdo aplicável deve ser preenchido ou possuir declaração explícita
  de ausência;
- observações e ocorrências mantêm as opções `Sem observações` e
  `Sem alterações`;
- cada linha deve conter uma ocupação ou a declaração `Livre`;
- EOTs disponíveis e avariados devem ser descritos ou declarados como nenhum;
- a ausência de rádios utilizados deve ser marcada explicitamente;
- detalhes condicionais do TECON que não se aplicam não devem aparecer na
  revisão;
- rascunhos antigos incompletos devem ser apresentados como pendentes de
  correção e não podem ser confirmados pela interface.

## Compatibilidade

- nenhum campo, endpoint ou migration é adicionado;
- as declarações usam os campos textuais e listas já existentes;
- respostas históricas continuam aceitando valores nulos para permitir a
  consulta e correção de registros anteriores;
- a API passa a rejeitar novos payloads com conteúdo obrigatório vazio.

## Critérios de aceite

- [x] validação do navegador exige preenchimento ou escolha explícita;
- [x] validação do backend rejeita registros, equipe, linhas e EOTs vazios;
- [x] revisão não apresenta `Não informado`;
- [x] detalhes condicionais não aplicáveis ficam ocultos;
- [x] confirmação de rascunho incompleto fica bloqueada na interface;
- [x] testes direcionados cobrem os novos comportamentos;
- [x] suítes completas, lint, tipagem, formatação e build aprovados.

## Evidências

- baseline: 31 testes de backend e 8 testes React aprovados;
- após a alteração: 27 testes direcionados de backend e 9 testes direcionados
  de React aprovados;
- suíte React completa: 34 testes aprovados;
- suíte backend inicial: 170 aprovados e 14 fixtures antigas corretamente
  identificadas para atualização.
- suíte final de backend: 184 testes aprovados;
- suíte final de frontend: 32 testes aprovados;
- Ruff, mypy, pre-commit, ESLint, TypeScript, Prettier e build Vite aprovados;
- a expressão `Não informado` foi removida da revisão, do histórico e das
  exportações; lacunas históricas são sinalizadas como pendentes de correção.
- a primeira execução do E2E no PR confirmou que o navegador bloqueia o envio
  sem as novas declarações; o roteiro foi atualizado para marcá-las;
- segunda execução do E2E aprovada com os seis cenários críticos no Chromium.
