# 0004 — Fronteira explícita de transações

Status: Aceito

## Contexto

Criação e edição de passagens envolvem múltiplas escritas que devem confirmar
ou falhar juntas, especialmente o snapshot de histórico e o estado atualizado.
Commits espalhados tornariam atomicidade e rollback difíceis de verificar.

## Decisão

Uma sessão SQLAlchemy é criada por requisição e injetada nos repositories. O
repository encapsula queries, `add` e `flush`; `TransacaoSQLAlchemy` centraliza
`commit`, `rollback` e `refresh`. O service coordena o caso de uso sem conhecer
detalhes HTTP.

## Alternativas consideradas

- commit dentro de cada método de repository;
- commit direto nos controllers;
- unit of work mais abstrata antes de existir mais de um mecanismo persistente.

## Consequências

As operações compostas ficam atômicas e testáveis, e falhas SQLAlchemy são
traduzidas sem vazar detalhes. Repository e transação ainda conhecem SQLAlchemy;
uma abstração adicional só será criada se outra implementação justificar o custo.
