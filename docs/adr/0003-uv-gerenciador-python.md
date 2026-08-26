# 0003 — uv como gerenciador Python

Status: Aceito

## Contexto

Requirements manuais não garantiam uma resolução única entre desenvolvimento,
CI e Docker. O projeto precisa separar dependências diretas de runtime e de
desenvolvimento, preservando compatibilidade com ferramentas baseadas em pip.

## Decisão

Usar `pyproject.toml` como manifesto, `uv.lock` como resolução reproduzível e
`uv sync --frozen` em desenvolvimento e CI. Os requirements com hashes são
exports do lockfile para Docker e compatibilidade; não são editados à mão.

## Alternativas consideradas

- requirements mantidos manualmente;
- Poetry ou Pipenv com seus próprios formatos de lock;
- pip-tools como fonte primária da resolução.

## Consequências

Instalações ficam rápidas e determinísticas, com grupos claros. Colaboradores
precisam instalar `uv`, e qualquer alteração de dependência exige atualizar e
validar lock e exports na mesma entrega.
