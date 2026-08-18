# Dependências reproduzíveis

Status: `CONCLUÍDA`

## Objetivo
Tornar instalação e atualização do backend reproduzíveis.

## Escopo
- classificar dependências diretas versus transitivas;
- consolidar dependências diretas no `pyproject.toml`;
- avaliar/adotar `uv` para lock;
- gerar lockfile;
- definir grupos dev/test;
- decidir estratégia transitória para `requirements.txt`;
- documentar instalação no Windows.

## Critérios de aceite
- [x] ambiente limpo instala com comando documentado;
- [x] lockfile versionado;
- [x] runtime e dev separados;
- [x] testes passam em ambiente reconstruído;
- [x] `requirements.txt` não entra em conflito com o manifesto.

## Evidências

- Branch: `chore/reproducible-dependencies`
- Commits: `8a66f7e` e commit de fechamento desta documentação.
- Testes antes: 100 aprovados.
- Testes depois: 100 aprovados no ambiente atual e 100 aprovados em ambiente
  temporário reconstruído exclusivamente com `uv sync --frozen`.
- Lint: `ruff check .` e `ruff format --check .` aprovados.
- Type-check: `mypy` aprovado em 21 arquivos de produção.
- Observações:
  - `uv.lock` registra 55 pacotes para Python 3.13;
  - dependências diretas de runtime estão em `[project.dependencies]`;
  - dependências de teste e desenvolvimento estão nos grupos `test` e `dev`;
  - versões transitivas do baseline anterior foram preservadas como constraints
    para impedir atualizações funcionais involuntárias;
  - `backend/requirements.txt` e `backend/requirements-dev.txt` são exports com
    hashes gerados do lockfile e não devem ser editados manualmente;
  - `uv lock --check`, pre-commit e verificação de compatibilidade dos 54 pacotes
    instalados no ambiente reconstruído foram aprovados;
  - cobertura total permaneceu em 93%;
  - nenhuma linha de produção, contrato HTTP ou regra de negócio foi alterada.
