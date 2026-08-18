# Contrato de responses e erros

Status: `TODO`

## Objetivo
Padronizar a borda HTTP sem espalhar regras de transporte.

## Escopo
- inventariar formatos atuais;
- criar schemas de erro;
- criar exception handlers;
- introduzir exceções de aplicação/domínio;
- mapear status codes;
- definir estratégia de envelope de sucesso;
- preservar compatibilidade com frontend atual.

## Critérios de aceite
- [ ] service novo não precisa lançar `HTTPException`;
- [ ] erros conhecidos têm `code` estável;
- [ ] status codes estão documentados;
- [ ] OpenAPI mostra responses;
- [ ] contratos existentes não foram quebrados silenciosamente.

## Evidências

Preencher ao executar a task:

- Branch:
- Commits:
- Testes antes:
- Testes depois:
- Lint:
- Type-check:
- Observações:
