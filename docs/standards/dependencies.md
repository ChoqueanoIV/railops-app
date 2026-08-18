# Gerenciamento de dependências

## Backend

Estado atual: `requirements.txt`.

Alvo:
- `pyproject.toml` como manifesto;
- lockfile;
- grupos de dependência;
- ferramenta única de instalação/lock.

Avaliar `uv`.

Migração deve manter um caminho de instalação documentado e reproduzível.

Grupos conceituais:

```text
runtime:
  fastapi
  sqlalchemy
  alembic
  pydantic
  driver postgres
  auth

dev/test:
  pytest
  pytest-cov
  ruff
  mypy
  pre-commit
  cliente de teste
```

Não copiar automaticamente todas as dependências transitivas atuais para o manifesto principal.

## Frontend

Usar `package.json` + lockfile versionado.

Separar dependencies de devDependencies.

Não instalar pacote sem justificativa técnica.

## Atualizações

Atualizações grandes de versão devem ser separadas das refatorações arquiteturais.
