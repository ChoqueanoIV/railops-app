# RailOps — Instruções para agentes de código

## Objetivo do projeto

Evoluir o RailOps com segurança, aumentando a maturidade arquitetural, qualidade, testabilidade e manutenibilidade sem alterar regras de negócio já existentes sem uma task explícita.

O projeto atual possui backend em Python/FastAPI/Pydantic/SQLAlchemy/Alembic, PostgreSQL, autenticação JWT, testes Pytest e frontend legado em HTML/CSS/JavaScript.

## Regra principal

**Refatoração não é mudança de comportamento.**

Antes de mover, renomear ou reescrever código existente:

1. Identifique o comportamento atual.
2. Localize ou crie testes de caracterização.
3. Execute os testes antes da alteração.
4. Faça a menor alteração estrutural possível.
5. Execute novamente testes, lint e type-check.
6. Só considere concluído quando o comportamento observado permanecer equivalente.

Nunca altere regra de negócio apenas para "melhorar arquitetura".

## Estratégia de evolução

A evolução deve acontecer incrementalmente, por task, evitando big bang.

Ordem preferencial:

1. baseline e testes de caracterização;
2. ferramentas de qualidade;
3. gerenciamento de dependências;
4. configuração tipada;
5. contratos HTTP e tratamento de erros;
6. arquitetura backend por feature;
7. repositories e unit of work/sessão;
8. services/use cases;
9. controllers/routers;
10. migrations;
11. observabilidade e segurança;
12. Docker;
13. frontend React;
14. CI;
15. README e documentação final.

## Backend — responsabilidades

### Controller / Router
Pode:
- receber request;
- validar payload via schema;
- resolver dependências;
- chamar um único caso de uso/service de alto nível;
- converter saída para response schema;
- definir status HTTP;
- declarar documentação OpenAPI.

Não pode:
- conter query SQL/SQLAlchemy;
- conter regra de negócio;
- realizar commit/rollback diretamente;
- implementar autenticação fora das dependências próprias;
- montar respostas ad hoc diferentes em cada endpoint.

### Service / Use Case
Responsável por:
- regras de negócio;
- orquestração;
- validações de domínio;
- decisões;
- transações quando aplicável;
- coordenação entre repositories.

Não deve conhecer FastAPI, Request, Response, status code ou detalhes HTTP.

### Repository
Responsável exclusivamente por persistência:
- buscar;
- listar;
- inserir;
- atualizar;
- remover;
- abstrair SQLAlchemy.

Não contém regra de negócio.

### Domain / Entity
Concentra conceitos do domínio e tipos sem dependência de HTTP.

Não usar Pydantic de transporte como entidade de domínio quando isso acoplar regras de negócio ao HTTP.

### ORM Model
Representa persistência SQLAlchemy e relacionamento com tabelas.

Evitar usar diretamente modelo ORM como payload de API.

### Schemas / DTOs
Pydantic para request/response e contratos de borda.

Separar, quando necessário:
- Create;
- Update;
- Read/Response;
- Filters;
- internal DTOs.

## Organização por feature

Preferir arquitetura orientada a feature conforme a migração avançar.

Estrutura-alvo sugerida:

```text
backend/
  app/
    api/
      dependencies/
      errors/
      responses/
      router.py
    core/
      config.py
      database.py
      security.py
      logging.py
    features/
      auth/
        controller.py
        schemas.py
        service.py
        repository.py
        models.py
        entities.py
        exceptions.py
      passagens/
        controller.py
        schemas.py
        service.py
        repository.py
        models.py
        entities.py
        exceptions.py
      tecon/
        ...
    shared/
      domain/
      persistence/
      types/
      utils/
    main.py
  alembic/
  tests/
    unit/
    integration/
    api/
```

A migração para essa estrutura deve ser gradual. Não mover tudo de uma vez.

## API REST

- Recursos em substantivos.
- Versão da API preferencialmente em `/api/v1`.
- Métodos HTTP devem respeitar semântica REST.
- Responses devem possuir schema documentado.
- Erros devem seguir envelope único.
- Não retornar stack trace ao cliente.
- Não vazar detalhes de banco.
- Usar códigos HTTP coerentes.
- Swagger/OpenAPI deve permanecer funcional.

Envelope de sucesso sugerido:

```json
{
  "data": {},
  "meta": {}
}
```

Para coleção:

```json
{
  "data": [],
  "meta": {
    "total": 0
  }
}
```

Envelope de erro sugerido:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Recurso não encontrado",
    "details": null
  }
}
```

Não introduzir envelope global sem antes garantir compatibilidade com o frontend atual. Se houver quebra de contrato, criar versão nova da API ou adaptar por etapas.

## Tipagem Python

Todo código novo ou alterado deve possuir type hints úteis.

Preferir:
- `str | None` em Python moderno;
- tipos concretos;
- Protocol quando abstração por contrato fizer sentido;
- generics somente quando reduzirem duplicação real.

Evitar:
- `Any` sem justificativa;
- casts para silenciar erro;
- `# type: ignore` indiscriminado;
- dicionários soltos onde um tipo estruturado melhora o contrato.

Type checker alvo: `mypy` em modo progressivamente estrito.

## Qualidade Python

Ferramentas alvo:
- Ruff para lint/imports;
- Black ou formatter do Ruff — escolher uma única estratégia;
- mypy para tipos;
- pytest;
- pytest-cov;
- pre-commit.

Não adicionar duas ferramentas para a mesma função sem necessidade.

## Dependências backend

Migrar progressivamente de `requirements.txt` manual para `pyproject.toml`.

Preferir grupo de dependências:
- runtime;
- dev;
- test.

Avaliar `uv` como gerenciador/lockfile, sem bloquear a execução tradicional até a migração estar estável.

Toda dependência nova deve:
1. ter propósito explícito;
2. evitar duplicar funcionalidade;
3. ser adicionada no manifesto correto;
4. ter lock atualizado;
5. passar testes;
6. ser documentada se impactar execução.

## Frontend

A modernização prevista é React + TypeScript.

Base alvo:
- React;
- TypeScript;
- Vite;
- React Router;
- ESLint;
- Prettier;
- aliases de import;
- Vitest;
- Testing Library.

Não migrar todas as telas de uma vez. Criar shell React e migrar fluxo por fluxo mantendo o legado acessível durante a transição quando necessário.

Estrutura sugerida:

```text
frontend/
  src/
    app/
    components/
    features/
    hooks/
    lib/
    routes/
    services/
    styles/
    types/
  tests/
  index.html
  package.json
  tsconfig.json
  vite.config.ts
  eslint.config.js
  .prettierrc
```

Usar imports absolutos, por exemplo `@/features/auth`.

## Testes

Pirâmide preferencial:
- muitos testes unitários;
- testes de integração para repository/banco;
- testes de API para contratos e status;
- poucos testes end-to-end críticos no futuro.

Toda refatoração de regra existente deve partir de teste de caracterização quando a cobertura atual não for suficiente.

Nomes de testes devem descrever comportamento.

Não testar detalhe de implementação sem necessidade.

## Banco e migrations

- Alembic é a fonte de versionamento do schema.
- Toda alteração estrutural no banco exige migration.
- Migration deve possuir upgrade e downgrade quando tecnicamente seguro.
- Não editar migration já aplicada em ambiente compartilhado.
- Evitar migration junto com refatoração não relacionada.

## Segurança

- Segredos somente por ambiente.
- Nunca versionar `.env`.
- Nunca logar PIN, senha, JWT completo ou segredo.
- Validar autenticação/autorização em dependências reutilizáveis.
- Hash de PIN/senha não pode ser reversível.
- Não reduzir segurança para facilitar testes.

## Git

Commits pequenos e semânticos, em PT-BR:

- `feat: ...`
- `fix: ...`
- `refactor: ...`
- `test: ...`
- `docs: ...`
- `chore: ...`
- `ci: ...`

Não misturar refatoração estrutural com feature funcional no mesmo commit.

## Antes de concluir uma task

Executar, conforme a área alterada:

Backend:
```bash
pytest
ruff check .
mypy backend
```

Frontend:
```bash
npm run lint
npm run typecheck
npm test
npm run build
```

Se um comando ainda não existir, a task responsável por criá-lo deve documentar isso.

## Definição de pronto

Uma task só termina quando:
- critérios de aceite foram cumpridos;
- regra de negócio permaneceu equivalente, salvo requisito explícito;
- testes foram atualizados;
- lint passou;
- type-check passou quando já habilitado;
- documentação relevante foi atualizada;
- não existem secrets ou artefatos temporários;
- diff foi revisado;
- task correspondente em `docs/tasks/` foi atualizada.
