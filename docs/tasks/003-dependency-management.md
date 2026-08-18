# Dependências reproduzíveis

Status: `TODO`

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
- [ ] ambiente limpo instala com comando documentado;
- [ ] lockfile versionado;
- [ ] runtime e dev separados;
- [ ] testes passam em ambiente reconstruído;
- [ ] `requirements.txt` não entra em conflito com o manifesto.

## Evidências

Preencher ao executar a task:

- Branch:
- Commits:
- Testes antes:
- Testes depois:
- Lint:
- Type-check:
- Observações:
