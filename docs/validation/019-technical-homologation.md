# Homologação técnica da Task 019

Data: 28/08/2026

Branch: `test/homologacao-operacional`

## Ambiente

- Windows com Docker Desktop 29.7.2 e Compose 5.4.0;
- PostgreSQL 17 em volume local recriado;
- backend construído pelo `backend/Dockerfile` e executado como container;
- frontend React executado pelo Vite em `127.0.0.1:5173`;
- migration `d7e9f2a3b4c5` aplicada no banco limpo.

## Validações aprovadas

- `/health`, `/ready` e `/docs` responderam HTTP 200;
- primeiro acesso, definição de PIN, login, logout e proteção de rota;
- seleção de Brisamar e TECON;
- criação de Brisamar validada pela API;
- consulta e carregamento do Brisamar no React;
- identidade da passagem bloqueada durante a edição;
- edição autorizada do Brisamar durante o turno noturno;
- confirmação da edição com terminal, data, turma, turno e protocolo;
- criação de TECON sem atendimento pelo React;
- criação de TECON com atendimento da Área 1 pela API;
- consulta do TECON com atendimento no React, preservando horários e campos;
- identidade da passagem TECON bloqueada durante a edição;
- confirmação sem link de edição para passagem fora da janela permitida;
- 134 testes backend, cobertura de 94%, Ruff, formatter e mypy;
- 13 testes frontend, ESLint, Prettier, TypeScript e build Vite.

## Defeito corrigido — severidade alta

### Handler de validação transformava 422 em 500

Ao receber uma combinação que falha em um `model_validator` do Pydantic, o
`RequestValidationError.errors()` inclui um objeto `ValueError` em `ctx`. O
handler em `app/api/errors.py` envia essa estrutura diretamente ao
`JSONResponse`; o encoder JSON falha e a API devolve `500`.

Reprodução:

1. autenticar um usuário;
2. enviar `POST /passagens/tecon` com estrutura válida, mas
   `houve_atendimento=false` e `area1_atendida=true`;
3. observar HTTP `500 INTERNAL_SERVER_ERROR` em vez de `422`;
4. no React, observar a mensagem genérica de falha de conexão.

Impacto:

- o fluxo válido permanece disponível;
- combinações condicionais inválidas podem produzir erro interno;
- o usuário não recebe orientação sobre o campo que precisa corrigir;
- o contrato documentado de validação HTTP 422 não é preservado.

A correção foi implementada isoladamente na Task 019A e integrada pelo PR #39.
O cenário inválido foi repetido após a integração: a API devolveu HTTP `422`
com detalhes serializáveis e o React exibiu "Dados da requisição inválidos",
sem erro `500` nem falsa falha de conexão.

## Limitação da automação de interface

Durante a retomada, o controlador do navegador não manteve no estado React os
valores digitados nos campos nativos `date` e `time`. O mesmo payload completo
foi aceito pela API e depois carregado corretamente no formulário React. Essa
limitação pertence à automação usada na homologação e não foi reproduzida no
uso manual da interface.

## Observações de UX

- primeiro acesso, login, seleção de terminal e confirmação são claros;
- formulários extensos dependem da validação nativa do navegador para campos
  obrigatórios;
- quando a API devolve erro de validação, a tela mostra somente uma mensagem
  geral e não associa o problema ao campo;
- a data deve continuar representando o início do turno, inclusive no noturno.

## Pendências humanas

- executar os fluxos com manobradores ou avaliadores representativos;
- registrar dúvidas de linguagem, ordem dos campos e uso em tela pequena;
- decidir público, visibilidade, filtros e paginação para a Task 020;
- decidir quem pode consultar autores e snapshots de alterações;
- definir finalidade e formato de relatórios futuros.

## Decisões para o contrato de consulta

- Público autorizado: todos os manobradores autenticados;
- Perfis adicionais autorizados: Instrutores e Monitores de Qualidade,
  identificados por matrículas que serão cadastradas posteriormente;
- Escopo: consulta de passagens confirmadas de Brisamar e TECON,
  independentemente da turma do usuário;
- Permissão após confirmação final: somente leitura, sem edição para nenhum dos
  públicos acima;
- Segurança documental: matrículas reais dos perfis especiais não devem ser
  registradas nos documentos versionados.

## Achados da validação humana

### Brisamar não representa integralmente L22 e L24 — severidade alta

- Perfil: manobrador, validação em cenário operacional realista;
- Fluxo: preenchimento da ocupação das linhas do Pátio Brisamar;
- Resultado: defeito funcional;
- Comportamento atual: cada uma das linhas 22 e 24 aceita uma única descrição
  de vagões e obriga escolher `SUP` ou `INF`;
- Comportamento necessário: permitir registrar vagões simultaneamente nas
  posições superior e inferior de L22 e L24;
- Lacuna adicional: incluir campos independentes para `Travessão L22` e
  `Travessão L24`;
- Impacto: uma passagem pode omitir parte da ocupação real do pátio e entregar
  informação operacional incompleta ao turno seguinte;
- Classificação: alta, pois existe perda potencial de informação operacional;
- Encaminhamento: corrigir em task isolada, com migration, testes e leitura
  compatível das passagens existentes. Não alterar o modelo durante a sessão
  de homologação.

### Confirmação não reconhece os dois terminais concluídos — severidade média

- Perfil: manobrador, validação do fluxo completo dos dois terminais;
- Fluxo: confirmação após registrar Brisamar e TECON;
- Resultado: lacuna funcional e de navegação;
- Comportamento atual: toda confirmação oferece `Preencher o outro terminal`,
  independentemente de o outro terminal já ter sido registrado;
- Causa confirmada: a tela usa apenas o terminal da última passagem e não
  mantém nem consulta o estado de conclusão do conjunto Brisamar + TECON;
- Comportamento necessário: após o primeiro terminal, oferecer o preenchimento
  do terminal pendente; após o segundo, exibir uma revisão consolidada de toda
  a passagem de Brisamar e TECON antes da confirmação definitiva;
- Impacto: o usuário pode entender que ainda existe uma etapa obrigatória ou
  iniciar um preenchimento duplicado;
- Classificação: média, pois confunde a conclusão do fluxo, mas não altera um
  registro já salvo;
- Decisão de UX: a revisão deve permitir conferir todos os dados dos dois
  terminais antes de confirmar;
- Decisão de negócio: a confirmação final encerra o ciclo e bloqueia
  imediatamente qualquer edição posterior em Brisamar e TECON, mesmo que a
  janela de edição original ainda esteja aberta;
- Decisão técnica pendente: definir se o primeiro preenchimento será salvo como
  rascunho no servidor ou persistido definitivamente antes da revisão, além de
  identificar que as duas passagens pertencem ao mesmo ciclo de turno.
