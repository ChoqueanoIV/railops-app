---
name: railops-tests
description: Use ao criar, reorganizar ou revisar testes do RailOps, especialmente testes de caracterização antes de refatorações e testes unitários, integração, API e cobertura.
---

# Testes RailOps

Antes de refatorar:
- capture comportamento existente;
- cubra caminhos feliz, inválido e bordas importantes;
- prefira asserts observáveis pelo consumidor.

Classifique testes:
- unit: sem I/O real;
- integration: banco/repository;
- api: contrato HTTP;
- e2e: somente fluxos críticos quando introduzido.

Evite mocks profundos de detalhes internos.
Fixtures devem ser pequenas e legíveis.
Não reduzir asserts apenas para fazer teste passar.
