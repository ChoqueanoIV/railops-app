---
name: railops-backend-architecture
description: Use ao trabalhar na arquitetura Python/FastAPI do RailOps: controllers, services, repositories, schemas, domínio, entidades, SQLAlchemy, injeção de dependência e separação por feature.
---

# Arquitetura backend RailOps

Aplique a direção de dependências:

`controller -> service -> repository -> persistence`

Regras:
- controller: HTTP e payload;
- service: negócio/orquestração;
- repository: persistência;
- domain/entity: conceitos do negócio;
- ORM model: banco;
- schema: contrato de entrada/saída.

Não usar `HTTPException` em service novo.
Não fazer query SQLAlchemy em controller.
Não usar modelo ORM como contrato HTTP sem justificativa.
Preferir dependency injection explícita.
Evitar abstrações genéricas antes de existirem dois ou mais usos concretos.
