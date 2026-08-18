# Padrões backend

## Python

Usar type hints em código novo/alterado.

Evitar `Any`.

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
