# Serialização dos erros de validação

Status: `CONCLUÍDA`

## Objetivo

Impedir que erros condicionais do Pydantic sejam convertidos em HTTP `500`
quando o contexto da validação contém um objeto `ValueError`.

## Escopo

- reproduzir a falha observada durante a homologação da Task 019;
- converter os detalhes da validação para valores serializáveis;
- preservar `detail` e o envelope `error` já consumidos pelos clientes;
- adicionar teste de regressão;
- validar o cenário real no Docker.

## Fora do escopo

- alterar regras de Brisamar ou TECON;
- alterar mensagens ou status de validações já serializáveis;
- modificar formulários do frontend;
- concluir a homologação humana da Task 019.

## Critérios de aceite

- [x] validação com `ValueError` no contexto retorna HTTP `422`;
- [x] `detail` continua sendo uma lista compatível;
- [x] `error.code` permanece `REQUEST_VALIDATION_ERROR`;
- [x] detalhes do erro podem ser codificados como JSON;
- [x] teste de regressão e suíte completa aprovados;
- [x] nenhuma regra de negócio alterada.

## Evidências

- Branch: `fix/validacao-422-serializavel`.
- Commit funcional: `22f80d7` (`fix: preserva 422 em erros condicionais`).
- Teste antes: novo caso falhou com `TypeError: Object of type ValueError is
  not JSON serializable`.
- Testes depois: 134 aprovados, cobertura backend de 94%.
- Qualidade: Ruff lint, Ruff format, mypy e pre-commit aprovados.
- Docker: o payload TECON inválido que retornava `500` passou a retornar `422`,
  com `ctx.error` convertido para texto no envelope compatível.
- Observações: somente serialização de erro e teste foram alterados.
