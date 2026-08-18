# Observabilidade e hardening

Status: `TODO`

## Objetivo
Aumentar maturidade operacional sem mudar regra funcional.

## Escopo
- logging consistente;
- correlation/request id se necessário;
- health/readiness;
- CORS por configuração;
- headers e práticas seguras;
- revisão de JWT;
- revisão de PIN/hash;
- rate limiting somente após avaliar necessidade;
- tratamento seguro de exceções;
- auditoria de dependências.

## Critérios de aceite
- [ ] secrets nunca são logados;
- [ ] healthcheck não expõe dados sensíveis;
- [ ] erros 500 têm log útil e response seguro;
- [ ] mudanças de segurança possuem testes;
- [ ] qualquer mudança de comportamento é explicitada.

## Evidências

Preencher ao executar a task:

- Branch:
- Commits:
- Testes antes:
- Testes depois:
- Lint:
- Type-check:
- Observações:
