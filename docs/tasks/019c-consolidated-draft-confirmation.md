# Rascunho e confirmação consolidada da passagem

Status: `PLANEJADA`

## Objetivo

Transformar Brisamar e TECON em partes de um único ciclo de passagem, com
rascunho persistente, revisão completa e bloqueio definitivo após a confirmação
final.

## Dependência

- Tasks 019 e 019B concluídas;
- executar antes das tasks 020–026.

## Regras de negócio aprovadas

- o primeiro terminal preenchido deve permanecer como rascunho no servidor;
- o usuário deve preencher o terminal ainda pendente;
- antes da confirmação final, deve visualizar todos os dados de Brisamar e
  TECON em uma revisão consolidada;
- a revisão deve permitir voltar e corrigir qualquer um dos terminais;
- a confirmação final encerra o ciclo inteiro;
- depois da confirmação final, Brisamar e TECON ficam imediatamente bloqueados
  para edição, independentemente da janela anterior;
- passagens confirmadas permanecem disponíveis somente para consulta.

## Escopo

- caracterizar criação, edição, identidade e autorização atuais;
- definir e persistir a identidade do ciclo por data de início, turma e turno;
- modelar estados explícitos de rascunho e confirmado;
- garantir um único ciclo ativo compatível por identidade operacional;
- criar migrations sem invalidar passagens existentes;
- criar endpoints compatíveis para salvar rascunhos, consultar a revisão e
  confirmar definitivamente;
- aplicar transação segura na confirmação final;
- atualizar React com indicação de terminal concluído, terminal pendente,
  revisão consolidada, retorno para correção e confirmação;
- bloquear no backend qualquer edição posterior à confirmação;
- adicionar testes concorrentes e de autorização quando aplicável;
- validar recuperação do rascunho após recarregar ou reabrir a página.

## Fora do escopo

- listagem histórica e filtros da Task 021;
- relatórios e exportações;
- alterar os dados operacionais internos de cada terminal além da Task 019B;
- usar somente `sessionStorage` como fonte do estado do rascunho;
- excluir passagens antigas.

## Critérios de aceite

- [ ] o primeiro terminal salvo reaparece após recarregar a página;
- [ ] o sistema identifica e oferece somente o terminal pendente;
- [ ] os dois terminais aparecem integralmente na revisão;
- [ ] o usuário pode corrigir ambos antes da confirmação final;
- [ ] a confirmação final é atômica e idempotente;
- [ ] qualquer edição posterior é rejeitada pelo backend e ocultada no React;
- [ ] passagens anteriores à migration continuam consultáveis;
- [ ] falha parcial não deixa um ciclo falsamente confirmado;
- [ ] testes backend e frontend cobrem o fluxo completo e as rejeições;
- [ ] lint, tipos, build, Docker e documentação são aprovados;
- [ ] nenhuma regra fora deste requisito é alterada.

## Riscos principais

- associar registros existentes ao novo conceito de ciclo sem inventar dados;
- impedir duplicidade em requisições repetidas ou concorrentes;
- manter compatibilidade de consulta durante a transição;
- garantir que o bloqueio seja imposto no backend, não apenas na interface.

## Evidências

Preencher durante a execução.
