# Estratégia de testes

## Objetivo inicial

Aumentar confiança antes de refatorar.

## Níveis

### Unit
Testa regra isolada:
- services;
- domínio;
- helpers.

### Integration
Testa:
- repository;
- SQLAlchemy;
- migrations;
- constraints importantes.

### API
Testa:
- endpoint;
- autenticação;
- payload;
- status;
- contrato de response;
- exception mapping.

### Frontend
Testa:
- componentes;
- formulários;
- serviços HTTP;
- rotas críticas.

## Caracterização

Antes de refatorar código sem cobertura suficiente, criar teste que descreva o comportamento atual, mesmo que a arquitetura atual não seja ideal.

## Coverage

Adicionar relatório de cobertura.

Não transformar percentual em objetivo cego. Cobrir primeiro:
- autenticação;
- regras de passagem;
- autorização;
- validações;
- persistência crítica.
