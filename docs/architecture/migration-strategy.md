# Estratégia de migração arquitetural

## Por que não fazer big bang

O backend já possui comportamento implementado e testes. Uma troca completa de estrutura aumenta o risco de regressão, dificulta revisão e mistura decisões de arquitetura com mudança funcional.

## Estratégia strangler interna

Migrar feature por feature.

Exemplo:

1. deixar estrutura atual funcionando;
2. escolher `auth`;
3. criar testes de caracterização;
4. estabelecer novos contratos;
5. mover somente `auth`;
6. manter import/adapter temporário se necessário;
7. validar;
8. remover código legado da feature;
9. seguir para próxima feature.

## Regra de compatibilidade

Durante a migração:
- endpoint existente permanece;
- payload existente permanece;
- regra existente permanece;
- banco permanece compatível;
- Swagger permanece utilizável.

Mudanças incompatíveis devem ser uma task separada e explicitamente aprovada.
