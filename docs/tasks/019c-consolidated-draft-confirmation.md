# Rascunho e confirmação consolidada da passagem

Status: `INTEGRADA` — PR #42, merge `02e9683`

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

- [x] o primeiro terminal salvo reaparece após recarregar a página;
- [x] o sistema identifica e oferece somente o terminal pendente;
- [x] os dois terminais aparecem integralmente na revisão;
- [x] o usuário pode corrigir ambos antes da confirmação final;
- [x] a confirmação final é atômica e idempotente;
- [x] qualquer edição posterior é rejeitada pelo backend e ocultada no React;
- [x] passagens anteriores à migration continuam consultáveis;
- [x] falha parcial não deixa um ciclo falsamente confirmado;
- [x] testes backend e frontend cobrem o fluxo completo e as rejeições;
- [x] lint, tipos, build, Docker e documentação são aprovados;
- [x] nenhuma regra fora deste requisito é alterada.

## Riscos principais

- associar registros existentes ao novo conceito de ciclo sem inventar dados;
- impedir duplicidade em requisições repetidas ou concorrentes;
- manter compatibilidade de consulta durante a transição;
- garantir que o bloqueio seja imposto no backend, não apenas na interface.

## Evidências

- branch própria criada: `feat/rascunho-confirmacao-consolidada`;
- baseline anterior à alteração: 135 testes backend e 13 testes React
  aprovados;
- Ruff, mypy, ESLint, type-check TypeScript e build Vite aprovados no baseline;
- caracterização confirmou passagens independentes por terminal, ausência de
  ciclo/estado persistido e dependência da confirmação React em
  `sessionStorage`;
- testes TDD adicionados para exigir os dois terminais, confirmação atômica e
  idempotente, autoria do rascunho e bloqueio após confirmação;
- estado vermelho inicial confirmado pela ausência deliberada de
  `CicloPassagem` e `PassagemCicloService`, antes da implementação.
- núcleo inicial aprovado em 46 testes direcionados, com Ruff e mypy verdes;
- migration `f9a2b3c4d5e6` validada no banco Docker preservado com upgrade,
  downgrade e novo upgrade;
- as seis passagens anteriores permaneceram consultáveis e com `ciclo_id`
  nulo, sem associação retroativa inventada;
- backend Docker saudável no novo head após a validação reversível.
- criação de Brisamar e TECON vinculada ao mesmo rascunho pela identidade
  operacional, preservando os endpoints de criação existentes;
- contratos autenticados adicionados para recuperar o rascunho, consultar a
  revisão consolidada e confirmar definitivamente o ciclo;
- resposta de criação ampliada de forma compatível com `ciclo_id` e terminal
  pendente;
- suíte completa do backend aprovada com 144 testes, além de Ruff e mypy.
- React direciona automaticamente ao terminal pendente usando o `ciclo_id` e
  recupera a identidade do turno no servidor após recarga;
- revisão consolidada exibe Brisamar e TECON integralmente, oferece retorno
  para correção durante o rascunho e confirmação final única;
- após confirmação, a interface passa a somente leitura e informa o bloqueio
  dos dois terminais;
- fallback legado mantido para confirmações antigas sem `ciclo_id`;
- frontend aprovado com 14 testes, ESLint, Prettier, type-check e build Vite.
- fluxo integrado Docker validou: TECON pendente após Brisamar, recuperação do
  rascunho, revisão com dois terminais, correção prévia e confirmação final;
- segunda confirmação retornou o mesmo `confirmado_em`, comprovando
  idempotência;
- edição posterior rejeitada pelo backend com HTTP 400 e código
  `PASSAGEM_UPDATE_INVALID`;
- criação concorrente da mesma identidade serializada por advisory lock
  transacional no PostgreSQL;
- ciclo temporário de homologação removido em transação; as seis passagens
  anteriores permaneceram intactas.
