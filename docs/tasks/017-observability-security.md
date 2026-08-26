# Observabilidade e hardening

Status: `CONCLUÍDA`

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
- [x] secrets nunca são logados;
- [x] healthcheck não expõe dados sensíveis;
- [x] erros 500 têm log útil e response seguro;
- [x] mudanças de segurança possuem testes;
- [x] qualquer mudança de comportamento é explicitada.

## Evidências

Preencher ao executar a task:

- Branch: `feat/observabilidade-seguranca`
- Commits: preenchido após o commit da entrega.
- Testes antes: backend 123 aprovados, cobertura 93,70%; frontend 13 aprovados.
- Testes depois: backend 133 aprovados, cobertura 94,06%; frontend 13 aprovados.
- Lint: Ruff, Ruff format, pre-commit, ESLint e Prettier aprovados.
- Type-check: mypy e TypeScript aprovados; build Vite aprovado.
- Observações: adicionados logs JSON sem payloads ou credenciais, request ID,
  headers defensivos, `/ready`, resposta segura para falhas inesperadas e
  healthcheck Docker por prontidão. Tokens sem `exp` são rejeitados; produção
  exige segredo JWT de 32 bytes e rejeita CORS `*`. `pip-audit` sobre o export
  hashado de runtime e `npm audit --omit=dev` não encontraram vulnerabilidades
  conhecidas em 26/08/2026. PIN e código de ativação continuam protegidos por
  bcrypt. Rate limiting foi adiado: requer política operacional de tentativas,
  identificação confiável do cliente atrás de proxy e armazenamento
  compartilhado; implementá-lo localmente agora poderia bloquear usuários
  legítimos ou divergir entre réplicas. A única mudança HTTP aditiva é
  `GET /ready`; regras de negócio e respostas dos endpoints existentes foram
  preservadas.
