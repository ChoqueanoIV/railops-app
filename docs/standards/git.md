# Git e entrega

## Branches

Sugestão:

```text
refactor/backend-architecture
chore/python-tooling
test/characterization
feat/react-shell
docs/readme
```

Quando houver número de issue/task, prefixar conforme o fluxo adotado no board.

## Commits

Semantic/Conventional Commit em PT-BR.

Exemplos:

```text
test: adiciona caracterização dos endpoints de passagem
chore: configura ruff e mypy no backend
refactor: separa persistência da regra de autenticação
feat: cria shell React com TypeScript e Vite
docs: atualiza instruções de execução local
```

## PR

Cada PR deve:
- ter objetivo único;
- listar impacto;
- evidenciar testes;
- indicar risco;
- evitar mudanças de formatação não relacionadas.
