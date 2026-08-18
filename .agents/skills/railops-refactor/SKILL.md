---
name: railops-refactor
description: Use para refatorações arquiteturais no RailOps que devem preservar comportamento, incluindo mover código, separar camadas, reduzir acoplamento e organizar features. Não use para implementar uma nova regra de negócio.
---

# Refatoração segura do RailOps

1. Leia `AGENTS.md`.
2. Leia a task ativa em `docs/tasks/`.
3. Mapeie o fluxo atual antes de editar.
4. Identifique testes existentes.
5. Se o comportamento relevante não estiver coberto, crie primeiro teste de caracterização.
6. Faça uma única refatoração conceitual por vez.
7. Não altere request/response público sem critério explícito.
8. Não mude schema do banco sem migration.
9. Rode os checks aplicáveis.
10. Resuma no final:
   - arquivos alterados;
   - comportamento preservado;
   - testes executados;
   - riscos/restos.
