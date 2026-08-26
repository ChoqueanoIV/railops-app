# Homologação técnica da Task 019

Data: 26/08/2026

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
- confirmação sem link de edição para passagem fora da janela permitida;
- 133 testes backend, cobertura de 94%, Ruff, formatter e mypy;
- 13 testes frontend, ESLint, Prettier, TypeScript e build Vite.

## Defeito encontrado — severidade alta

### Handler de validação pode transformar 422 em 500

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

A correção não foi aplicada durante a homologação. Ela deve sanitizar os
detalhes da validação para tipos serializáveis e ganhar teste de regressão de
API antes da continuação da Task 019.

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
