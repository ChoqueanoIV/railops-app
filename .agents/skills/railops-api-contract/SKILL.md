---
name: railops-api-contract
description: Use ao modificar endpoints FastAPI, schemas Pydantic, códigos HTTP, envelopes de response, documentação Swagger/OpenAPI ou tratamento central de erros do RailOps.
---

# Contrato REST RailOps

Preserve contratos existentes até existir uma task de versão/migração.

Para código novo:
- usar schemas de response;
- declarar status code;
- padronizar erro;
- documentar responses OpenAPI;
- não retornar exceção interna;
- não vazar banco/stack trace.

Se a padronização de envelope quebrar frontend existente, introduza compatibilidade ou endpoint versionado.
