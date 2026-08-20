# Padrão REST

## Base

Preferência futura:

```text
/api/v1
```

## Resources

Usar substantivos e coleções previsíveis.

Exemplos conceituais:

```text
POST   /api/v1/auth/login
GET    /api/v1/passagens
POST   /api/v1/passagens
GET    /api/v1/passagens/{id}
PATCH  /api/v1/passagens/{id}
```

Ajustar nomes à linguagem de domínio real.

## Status

- 200 consulta/alteração com corpo;
- 201 criação;
- 204 operação sem corpo;
- 400 request semanticamente inválido quando adequado;
- 401 não autenticado;
- 403 não autorizado;
- 404 recurso inexistente;
- 409 conflito;
- 422 validação de payload;
- 500 falha inesperada.

## Erros

Formato atual de transição:

```json
{
  "detail": "Passagem não encontrada.",
  "error": {
    "code": "PASSAGEM_NOT_FOUND",
    "message": "Passagem não encontrada.",
    "details": null
  }
}
```

O campo `detail` é mantido temporariamente para compatibilidade com o frontend
legado. Clientes novos devem consumir `error.code`, `error.message` e
`error.details`. Erros de validação mantêm a lista original em `detail` e usam o
código `REQUEST_VALIDATION_ERROR`.

### Códigos conhecidos

| Código | Status | Situação |
|---|---:|---|
| `INVALID_ACTIVATION_DATA` | 400 | Dados inválidos no primeiro acesso |
| `INVALID_CREDENTIALS` | 401 | Matrícula ou PIN inválidos |
| `NOT_AUTHENTICATED` | 401 | Token ausente, inválido ou expirado |
| `PASSAGEM_INVALID` | 400 | Regra inválida ao criar passagem |
| `PASSAGEM_UPDATE_INVALID` | 400 | Regra inválida ao editar passagem |
| `PASSAGEM_NOT_FOUND` | 404 | Passagem não encontrada na consulta |
| `REQUEST_VALIDATION_ERROR` | 422 | Payload ou parâmetro inválido |
| `HTTP_ERROR` | variável | Compatibilidade com erros HTTP legados |

## Sucesso

Objeto:

```json
{
  "data": {
    "id": 1
  },
  "meta": {}
}
```

Coleção:

```json
{
  "data": [],
  "meta": {
    "total": 0
  }
}
```

A introdução do envelope deve considerar compatibilidade do frontend legado.

## OpenAPI

Cada endpoint deve:
- ter summary;
- response model;
- status;
- erros relevantes documentados;
- exemplos quando úteis.
