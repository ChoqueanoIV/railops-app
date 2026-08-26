# 0008 — Docker local sem plataforma de deploy definida

Status: Aceito

## Contexto

O projeto precisa de execução reproduzível para API e PostgreSQL antes de haver
uma plataforma, topologia ou orçamento de produção definidos.

## Decisão

Manter Dockerfile multi-stage para a API e Compose para desenvolvimento local,
com PostgreSQL, migrations antes do Uvicorn, usuário não-root e readiness. O
frontend React continua executado separadamente. Não escolher ainda provedor,
orquestrador, TLS, proxy, banco gerenciado ou estratégia de publicação do React.

## Alternativas consideradas

- depender apenas de instalações locais de Python/PostgreSQL;
- incluir frontend e proxy no Compose antes de definir deploy;
- escolher antecipadamente uma plataforma de nuvem específica.

## Consequências

Desenvolvimento e avaliação têm ambiente repetível sem cristalizar decisões de
produção. O Compose não representa arquitetura de produção; deploy,
observabilidade externa, backups, TLS e escalabilidade exigirão requisitos e um
novo ADR antes da implementação.
