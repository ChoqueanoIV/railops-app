# 0005 — Modelos ORM como representação interna

Status: Aceito

## Contexto

O domínio atual é centrado em persistência relacional e ainda não possui lógica
que justifique duplicar cada modelo em entidade pura. Ao mesmo tempo, expor ORM
diretamente na API acoplaria transporte, sessão e banco.

## Decisão

Usar modelos SQLAlchemy como representação interna entre repository e service,
mantendo schemas Pydantic separados nas bordas HTTP. Regras permanecem nos
services e validações de transporte nos schemas. Introduzir entidades de domínio
independentes somente quando invariantes ou múltiplas persistências exigirem.

## Alternativas consideradas

- entidades puras e mapeadores para todos os modelos desde já;
- usar ORM diretamente como request e response;
- concentrar regras nos modelos SQLAlchemy.

## Consequências

Evita duplicação e mapeamento sem benefício atual, preservando contratos HTTP
tipados. Services continuam acoplados aos tipos ORM; esse custo é consciente e
deve ser revisto se o domínio ganhar comportamento independente da persistência.
