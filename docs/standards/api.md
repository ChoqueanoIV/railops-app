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

Formato alvo:

```json
{
  "error": {
    "code": "PASSAGEM_NOT_FOUND",
    "message": "Passagem não encontrada.",
    "details": null
  }
}
```

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
