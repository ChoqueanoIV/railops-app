# Fronteira de persistência e transações

## Responsabilidades atuais

- `get_db` cria uma única sessão SQLAlchemy por requisição e sempre a fecha;
- dependencies constroem services e repositories com essa mesma sessão;
- controllers recebem services e não importam SQLAlchemy;
- repositories encapsulam queries, `add` e `flush`;
- `TransacaoSQLAlchemy` é o único componente que executa `commit`, `rollback` e
  `refresh` nas operações migradas;
- services preservam regras e coordenam rollback quando uma edição falha antes
  da confirmação;
- falhas SQLAlchemy são convertidas em `PersistenciaError` sem mensagem interna.

## Limites de confirmação

- criação de passagem: catálogo, rádios e agregado são confirmados juntos;
- edição de passagem: lock, snapshot e novo estado pertencem à mesma transação;
- primeiro acesso: hash do PIN e invalidação do código são confirmados juntos;
- consultas não executam commit;
- `flush` pode obter identidade ou materializar registros, mas não encerra a
  transação.

O engine, `SessionLocal`, modelos, metadata e Alembic continuam usando a mesma
configuração PostgreSQL. Nenhuma sessão é criada dentro de uma operação de
repository.
