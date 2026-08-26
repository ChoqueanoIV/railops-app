# Padrões backend

## Python

Funções de produção devem possuir assinaturas completas. O mypy aplica
`disallow_untyped_defs = true` ao backend configurado.

Evitar `Any`, casts usados apenas para silenciar erros e `type: ignore` amplo.
Preferir `Self` em validators, unions explícitas para contratos alternativos e
`Protocol` somente em fronteiras que realmente precisam de abstração.

## FastAPI

- routers/controllers finos;
- dependencies para autenticação e sessão;
- exception handlers centrais;
- schemas explícitos.

## Configuração

Centralizar configuração de ambiente em objeto tipado.

Variáveis esperadas devem falhar cedo quando ausentes, salvo valores realmente opcionais.

## SQLAlchemy

- sessão controlada;
- repositories responsáveis por acesso;
- evitar query em service/controller;
- evitar lazy-loading inesperado em response.

## Logging e respostas operacionais

- usar logs JSON com evento e metadados explicitamente permitidos;
- correlacionar requisição e resposta por `X-Request-ID` validado;
- nunca registrar payload, Authorization, PIN, token, hash ou segredo;
- usar `/health` para liveness e `/ready` para prontidão do banco;
- devolver erro 500 genérico ao cliente e registrar contexto seguro no servidor.

## Imports

Imports absolutos do pacote.

Não usar manipulação de `sys.path` em runtime.
