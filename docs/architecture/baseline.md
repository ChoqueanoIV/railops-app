# Baseline de comportamento

Data da caracterização: **18/08/2026**

Branch: `test/baseline-characterization`

Base: `main` no merge `04a410f`

## Objetivo

Este documento congela o comportamento observável do RailOps antes da
evolução arquitetural. Ele descreve o sistema como existe hoje; não propõe
mudanças de regra, contrato ou tecnologia.

## Comandos e resultado inicial

O executável do `venv` localizado no OneDrive retorna acesso negado. A mesma
instalação foi executada com o Python 3.13 original e o `site-packages` do
ambiente virtual:

```powershell
$env:PYTHONPATH=(Resolve-Path 'venv/Lib/site-packages').Path
& 'C:\Users\Leandro CHOQUE\AppData\Local\Programs\Python\Python313\python.exe' -m pytest
```

Resultado antes dos novos testes de caracterização: **88 passed**.

Ruff, mypy e coverage ainda não estão configurados. Essa ausência é parte do
baseline e pertence às tasks de tooling e cobertura.

## Superfície HTTP atual

| Método | Caminho | Autenticação | Sucesso atual |
|---|---|---|---|
| `GET` | `/health` | não | `200 {"status":"ok"}` |
| `POST` | `/auth/primeiro-acesso` | não | `201 {"mensagem":"PIN definido com sucesso"}` |
| `POST` | `/auth/login` | não | `200 {"access_token":"...","token_type":"bearer"}` |
| `POST` | `/passagens/brisamar` | Bearer JWT | `201` com `id` e `mensagem` |
| `POST` | `/passagens/tecon` | Bearer JWT | `201` com `id` e `mensagem` |
| `GET` | `/passagens/{passagem_id}` | Bearer JWT | `200` com a passagem completa e `editavel` |
| `PUT` | `/passagens/{passagem_id}` | Bearer JWT | `200` com `id` e `mensagem` |

Não existe prefixo `/api/v1` nem envelope global de sucesso/erro. Erros de
negócio são retornados atualmente no formato padrão do FastAPI,
`{"detail":"mensagem"}`. Erros de validação usam `detail` como lista.

### Autenticação

`POST /auth/primeiro-acesso` recebe:

- `matricula`: exatamente 8 dígitos;
- `codigo_ativacao`: exatamente 6 dígitos;
- `pin`: exatamente 4 dígitos.

Dados de ativação inválidos, código reutilizado e usuário já ativado produzem
`400`. Payload inválido produz `422`.

`POST /auth/login` recebe matrícula de 8 dígitos e PIN de 4 dígitos. Login
válido gera JWT HS256 com `sub`, `matricula` e expiração de 480 minutos.
Matrícula inexistente, usuário sem PIN e PIN incorreto compartilham a mensagem
`Matrícula ou PIN inválidos.` e produzem `401`. Token inválido, expirado ou de
usuário inexistente não autentica a requisição.

### Criação de passagem

Os dois terminais recebem no núcleo:

- data de início do turno;
- turma `A`, `B`, `C` ou `D`;
- turno `DIURNO` ou `NOTURNO`;
- observações e relatório de ocorrências;
- uso do Mobile e justificativa quando ele não foi utilizado;
- equipe, ocupações de linhas, detalhe do terminal e rádios utilizados.

Matrícula de membro possui 8 dígitos. Rádio marcado com falha exige descrição.
Strings recebidas são aparadas. Campos extras são rejeitados.

#### Brisamar

- exige exatamente as linhas `16`, `18`, `20`, `22`, `24`, `26`, `28` e `30`;
- não aceita linha ausente ou duplicada;
- linhas `22` e `24` exigem `SUP` ou `INF`;
- as demais linhas rejeitam `SUP`/`INF`;
- quantidades de rádios, baterias e carregadores não podem ser negativas.

#### TECON

- exige exatamente `Viaduto/DM1A`, `L1`, `L2`, `Travessão`, `DM4`, `DM6`,
  `DM1`, `DM3` e `Funil/DM2`;
- nenhuma linha permite `SUP`/`INF`;
- observações e relatório de ocorrências são textos obrigatórios;
- sem atendimento, todos os campos específicos ficam nulos;
- com atendimento, informa carga mal posicionada e as Áreas 1 e 2;
- carga mal posicionada exige descrição;
- cada área atendida exige início e término; área não atendida rejeita horários.

### Consulta e edição

`GET /passagens/{id}` retorna núcleo, equipe, linhas, detalhe do terminal,
rádios e o booleano `editavel`. Qualquer usuário autenticado pode consultar; o
booleano apenas informa se o usuário atual satisfaz as regras de edição.
Registro inexistente retorna `404`.

`PUT /passagens/{id}` aceita o corpo de Brisamar ou TECON sem `data`, `turma`,
`turno`, `terminal` ou autor. Esses campos formam a identidade imutável da
passagem. O payload deve corresponder ao terminal persistido.

A edição é permitida somente:

- ao usuário que criou a passagem;
- durante o próprio turno;
- no diurno, de 07:00 inclusivo a 19:00 exclusivo;
- no noturno, de 19:00 inclusivo a 07:00 exclusivo do dia seguinte.

Para turno noturno, `data` é a data em que o turno começou às 19:00. Registros
legados sem turma/turno separados são somente leitura. A orientação de realizar
a passagem nos 15 minutos finais não é bloqueio de software.

Antes da mutação é criado um snapshot completo com versão sequencial, autor e
estado anterior. Snapshot e atualização pertencem à mesma transação; uma falha
desfaz ambos. Detalhes 1:1 e ocupações existentes são atualizados preservando a
identidade das linhas no banco.

## Persistência observada

- SQLAlchemy síncrono com PostgreSQL/Supabase;
- sessão injetada pelo FastAPI;
- Alembic como histórico de schema;
- migration head atual: `d7e9f2a3b4c5`;
- tabelas especializadas para detalhes Brisamar e TECON;
- tabela `passagem_servico_historico` com unicidade por passagem e versão;
- `turno_legado`, `turma` e `turno` anuláveis no ORM para compatibilidade;
- novos requests exigem turma e turno válidos.

## Frontend legado observado

O frontend é HTML/CSS/JavaScript sem build. O token JWT e a última confirmação
são guardados em `sessionStorage`. A URL da API é atualmente fixa em
`http://127.0.0.1:8000`.

Há telas de login, seleção de terminal, formulários Brisamar/TECON e
confirmação. Os formulários suportam criação e edição por query string
`?editar=<uuid>`. Em edição, consultam a passagem, bloqueiam data/turma/turno e
enviam o conteúdo permitido por `PUT`. A confirmação só oferece edição quando
a API devolve `editavel: true`.

## Cobertura de caracterização

Após esta task, a suíte cobre de forma observável:

- primeiro acesso, login, claims JWT e rejeições de autenticação;
- inventário OpenAPI, autenticação das rotas e status de sucesso;
- schemas e regras condicionais de Brisamar e TECON;
- montagem e persistência das passagens;
- autorização e limites exatos da janela de edição;
- snapshot anterior, versão e rollback;
- consulta detalhada, incompatibilidade de terminal e registros legados;
- health check.

## Buracos conhecidos, sem alteração nesta task

- não há cliente ASGI/TestClient configurado para testes HTTP completos;
- routers são caracterizados por chamada direta e pelo OpenAPI;
- não há banco PostgreSQL isolado integrado à suíte comum;
- migrations não possuem teste automatizado de upgrade/downgrade;
- o E2E real de edição foi executado manualmente, não faz parte do Pytest;
- não há testes automatizados do frontend legado;
- não há métrica de coverage configurada;
- Ruff e mypy ainda não estão instalados/configurados;
- a suíte ainda carrega configuração local de ambiente durante imports.

Esses itens são riscos registrados para as tasks posteriores. Corrigi-los na
task 001 alteraria tooling, dependências ou arquitetura e violaria seu escopo.
