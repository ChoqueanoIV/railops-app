# Configuração tipada e bootstrap da aplicação

Status: `CONCLUÍDA`

## Objetivo
Centralizar configuração e inicialização do FastAPI.

## Escopo
- criar configuração tipada;
- centralizar variáveis de ambiente;
- revisar criação de engine/session;
- mover bootstrap para `backend/app/main.py` se adequado;
- manter entrypoint compatível temporariamente quando necessário;
- preparar configuração por ambiente sem secrets versionados.

## Critérios de aceite
- [x] configuração possui tipos;
- [x] app inicia com configuração válida;
- [x] erro de variável obrigatória é claro;
- [x] testes não dependem de credenciais reais;
- [x] Swagger continua acessível.

## Evidências

- Branch: `refactor/typed-config-bootstrap`
- Commits: `2a06ef1` e commit de fechamento desta documentação.
- Testes antes: 100 aprovados.
- Testes depois: 105 aprovados; cobertura total de 94%.
- Lint: `ruff check .` e `ruff format --check .` aprovados.
- Type-check: `mypy` aprovado em 22 arquivos de produção.
- Observações:
  - `Configuracao` é tipada, imutável e carregada de forma centralizada;
  - `DATABASE_URL`, `JWT_SECRET_KEY`, ambiente, título da API e CORS estão
    centralizados sem valores secretos versionados;
  - `backend/app/main.py` contém a fábrica `criar_app`;
  - `backend/main.py` preserva compatibilidade com `uvicorn main:app`;
  - testes usam exclusivamente credenciais fictícias definidas no bootstrap;
  - `.env.example` e instruções de configuração foram adicionados;
  - inventário e respostas do OpenAPI permaneceram compatíveis com o baseline;
  - pre-commit aprovado e nenhuma regra de negócio foi alterada.
