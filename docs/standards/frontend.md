# Padrões frontend

## Stack alvo

- React;
- TypeScript;
- Vite;
- React Router;
- ESLint;
- Prettier;
- Vitest;
- Testing Library.

## Scripts esperados

```json
{
  "scripts": {
    "dev": "...",
    "build": "...",
    "lint": "...",
    "format": "...",
    "typecheck": "...",
    "test": "..."
  }
}
```

## Alias

Configurar:

```text
@/* -> src/*
```

Manter alias consistente em TypeScript, Vite, testes e ESLint.

## HTTP

Um único cliente em `src/services/api`.

## Componentes

Separar:
- UI reutilizável;
- feature;
- página/rota;
- acesso à API.

Não acoplar componente visual ao formato cru do backend quando um mapper simples resolver.
