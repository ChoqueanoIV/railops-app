# 0007 — Token de acesso em sessionStorage

Status: Aceito

## Contexto

A API entrega JWT bearer e não implementa cookies de sessão ou refresh token.
O frontend precisa manter autenticação durante a aba sem persistir a sessão
indefinidamente no dispositivo compartilhado.

## Decisão

Armazenar o access token em `sessionStorage`, acessado somente pelo módulo
`tokenStorage`. Enviá-lo no header Authorization e removê-lo em logout ou
resposta 401/403. Nunca registrar ou renderizar o token.

## Alternativas consideradas

- `localStorage`, com persistência entre sessões;
- token apenas em memória, perdido a cada recarga;
- cookie `HttpOnly`, que exigiria contrato de autenticação, CSRF e backend
  diferentes.

## Consequências

A sessão termina ao fechar a aba e sobrevive a recargas. Como qualquer storage
acessível por JavaScript, não protege contra XSS; CSP, dependências auditadas e
ausência de HTML não confiável continuam importantes. Migrar para cookie
`HttpOnly` exigirá ADR e mudança coordenada de contrato.
