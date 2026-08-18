---
name: railops-dependencies
description: Use para gerenciamento de dependências do RailOps, incluindo pyproject.toml, lockfile, requirements legados, uv/pip, package.json, npm, atualização de bibliotecas e auditoria de dependências.
---

# Dependências RailOps

Antes de adicionar uma biblioteca:
1. explique o problema que ela resolve;
2. verifique se a stack atual já resolve;
3. escolha dependência mantida e pequena;
4. adicione no grupo correto;
5. atualize lock;
6. execute testes;
7. não faça upgrade amplo sem task própria.

Backend: migrar gradualmente para `pyproject.toml`.
Frontend: `package.json` com scripts previsíveis e lockfile versionado.
