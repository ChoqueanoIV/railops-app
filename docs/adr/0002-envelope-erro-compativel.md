# 0002 — Envelope de erro compatível

Status: Aceito

## Contexto

Clientes existentes consumiam o campo `detail` do FastAPI. Um contrato de erro
estável precisa também oferecer código, mensagem e detalhes estruturados, sem
quebrar o frontend durante a migração.

## Decisão

Erros retornam simultaneamente `detail` e `error`, sendo `error` composto por
`code`, `message` e `details`. Clientes novos usam `error`; `detail` permanece
como compatibilidade temporária. Não adotar envelope global de sucesso nem
prefixo `/api/v1` até existir uma migração de contrato explicitamente aprovada.

## Alternativas consideradas

- manter somente `detail`;
- remover `detail` imediatamente;
- envelopar todas as respostas de sucesso e erro em uma única mudança.

## Consequências

O contrato ganha códigos estáveis e responses 500 seguros sem interromper os
clientes atuais. Há redundância temporária no payload; sua remoção será uma
mudança incompatível e exigirá versionamento ou migração coordenada.
