---
name: railops-migrations
description: Use quando uma task do RailOps altera schema PostgreSQL, modelos SQLAlchemy ou migrations Alembic.
---

# Migrations RailOps

- Toda mudança de schema exige Alembic.
- Não reescreva migration já compartilhada.
- Inspecione SQL gerado.
- Teste upgrade.
- Quando seguro, teste downgrade.
- Separe migration de refatorações não relacionadas.
- Dados de produção não devem ser apagados por conveniência de desenvolvimento.
