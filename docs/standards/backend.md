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

## Logging

Adicionar logging estruturado progressivamente.

Nunca logar secrets.

## Imports

Imports absolutos do pacote.

Não usar manipulação de `sys.path` em runtime.
