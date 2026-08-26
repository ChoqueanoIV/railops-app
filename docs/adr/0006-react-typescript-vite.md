# 0006 — React, TypeScript e Vite

Status: Aceito

## Contexto

O frontend original em HTML e JavaScript global dificultava reutilização,
tipagem de contratos e testes por fluxo. A migração precisava preservar uma
forma de comparação operacional sem interromper as telas existentes.

## Decisão

Adotar React, TypeScript, Vite e React Router, com Vitest e Testing Library. O
cliente HTTP é centralizado e as telas são migradas por fluxo para features. O
legado permanece como fallback temporário até validação e remoção deliberada.

## Alternativas consideradas

- continuar apenas com JavaScript sem build;
- reescrever todas as telas de uma vez;
- adotar um framework full-stack com renderização no servidor.

## Consequências

Contratos, rotas e componentes ficam testáveis e o build é reproduzível. O
projeto mantém temporariamente duas interfaces e uma cadeia Node adicional; a
remoção do legado requer validação operacional explícita.
