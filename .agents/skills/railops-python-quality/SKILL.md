---
name: railops-python-quality
description: Use ao configurar ou corrigir lint, formatter, imports, tipagem, mypy, Ruff, pyproject, pre-commit ou qualidade estática do backend Python.
---

# Qualidade Python RailOps

Objetivo:
- Ruff;
- formatter único;
- mypy progressivo;
- pytest + coverage;
- pre-commit.

Regras:
- não faça uma alteração massiva de formatação junto com mudança funcional;
- habilite regras gradualmente se o legado gerar muitos erros;
- todo `ignore` deve ser pontual e justificável;
- não introduza `Any` para contornar type-check.
