# Frontend — orientação específica

Estas regras complementam o `AGENTS.md` da raiz.

## Estratégia

O frontend atual é React + TypeScript. A implementação anterior em HTML, CSS e
JavaScript foi removida após homologação, e não deve ser reintroduzida como
atalho para mudanças funcionais.

## Stack alvo

- React
- TypeScript
- Vite
- React Router
- ESLint
- Prettier
- Vitest
- Testing Library

## Organização

Preferir feature-first para regras de tela:

```text
src/
  app/
  components/
  features/
    auth/
    passagens/
    tecon/
  services/
  routes/
  lib/
  hooks/
  styles/
  types/
```

## API

Criar um cliente HTTP central.

Componentes não devem espalhar `fetch` diretamente.

Normalizar:
- base URL;
- JWT;
- tratamento de 401/403;
- parsing de erro;
- timeout;
- tipos de request/response.

## TypeScript

Não usar `any` como saída fácil.

Dados vindos da API devem ter contratos tipados.

## Imports

Configurar alias `@/* -> src/*`.

Evitar caminhos como `../../../../`.

## Testes

Priorizar:
- componentes com comportamento;
- hooks;
- services de API;
- fluxos críticos de autenticação e formulários.
