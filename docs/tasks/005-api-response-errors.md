# Contrato de responses e erros

Status: `CONCLUÍDA`

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
- [x] service novo não precisa lançar `HTTPException`;
- [x] erros conhecidos têm `code` estável;
- [x] status codes estão documentados;
- [x] OpenAPI mostra responses;
- [x] contratos existentes não foram quebrados silenciosamente.

## Evidências

Preencher ao executar a task:

- Branch: `refactor/api-response-errors`
- Commits: `7308abe` (`refactor: padroniza erros da API`) e `dfa8808`
  (`docs: registra evidencias dos contratos HTTP`)
- Testes antes: `105 passed`
- Testes depois: `109 passed`; cobertura total de `94%`
- Lint: `ruff check backend` e hooks Ruff do pre-commit aprovados
- Type-check: `mypy` aprovado no escopo configurado no `pyproject.toml`
- Observações: o envelope estruturado foi introduzido de forma aditiva. O campo
  legado `detail`, os status HTTP e os corpos de sucesso foram preservados para
  manter compatibilidade com o frontend atual. A migração do envelope de sucesso
  permanece futura e deve ser versionada ou feita em etapas.
