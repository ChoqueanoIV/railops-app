# Tooling Python e pyproject

Status: `CONCLUÍDA`

## Objetivo
Criar uma base consistente de qualidade estática sem alterar runtime.

## Escopo
- introduzir `pyproject.toml`;
- configurar Ruff;
- configurar formatter;
- configurar mypy progressivo;
- configurar pytest no manifesto quando apropriado;
- adicionar `pytest-cov`;
- adicionar pre-commit;
- criar scripts/comandos documentados.

## Estratégia
Não habilitar um conjunto extremo de regras que gere refatoração massiva. Começar com baseline sustentável.

## Critérios de aceite
- [x] lint executa;
- [x] formatter executa;
- [x] mypy executa;
- [x] pytest executa;
- [x] coverage gera relatório;
- [x] pre-commit configurado;
- [x] nenhum diff funcional involuntário.

## Evidências

- Branch: `chore/python-tooling`
- Commits: `dd51af7` e commit de fechamento desta documentação.
- Testes antes: 100 aprovados.
- Testes depois: 100 aprovados; cobertura total de 93% com branch coverage.
- Lint: `python -m ruff check .` aprovado; `python -m ruff format --check .` aprovado.
- Type-check: `python -m mypy` aprovado em 21 arquivos de produção.
- Observações:
  - `python -m pre_commit run --all-files` aprovado;
  - `python -m pre_commit validate-config .pre-commit-config.yaml` aprovado;
  - `python -m pip check` sem dependências quebradas;
  - migrations existentes foram excluídas do baseline de Ruff para não alterar
    arquivos já aplicados;
  - exceções progressivas do mypy ficaram limitadas aos códigos já existentes em
    `app.services.passagem_service`, `app.routers.passagem_router` e modelos ORM;
  - mudanças nos arquivos Python foram somente formatação, ordenação de imports,
    remoção de BOM e remoção de um import não utilizado; contratos e regras de
    negócio permaneceram inalterados.
