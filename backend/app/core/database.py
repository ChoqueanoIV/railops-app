"""
Módulo responsável por configurar a conexão do SQLAlchemy com o banco
de dados PostgreSQL (Supabase), conforme ADR-004.

Este módulo NÃO contém nenhuma credencial diretamente. A string de
conexão é lida do arquivo .env (variável DATABASE_URL), que nunca é
versionado pelo Git.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import obter_variavel_obrigatoria

# Carrega as variáveis definidas no arquivo .env para o ambiente do
# processo Python atual. Precisa ser chamado antes de tentarmos ler
# qualquer variável com os.getenv().

# Lê a string de conexão a partir da variável de ambiente DATABASE_URL.
# Se a variável não existir (.env ausente ou mal configurado), levanta
# um erro claro e imediato, em vez de falhar silenciosamente mais tarde.
DATABASE_URL = obter_variavel_obrigatoria("DATABASE_URL")

# O "engine" é o objeto central do SQLAlchemy responsável por gerenciar
# a comunicação de baixo nível com o banco de dados (pool de conexões,
# execução de comandos SQL gerados pelo ORM, etc.).
engine = create_engine(DATABASE_URL)

# SessionLocal é uma "fábrica" de sessões. Cada sessão representa uma
# conversa individual com o banco (ex.: uma requisição HTTP inteira),
# dentro da qual podemos consultar, inserir ou atualizar dados.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base é a classe da qual todos os nossos modelos (tabelas) do
# SQLAlchemy vão herdar. É o que permite ao SQLAlchemy saber quais
# classes Python representam quais tabelas do banco.
Base = declarative_base()


def get_db():
    """
    Fornece uma sessão de banco de dados para uma requisição, e garante
    que ela seja fechada corretamente ao final, mesmo se ocorrer um
    erro no meio do caminho. Será usada pelas rotas do FastAPI através
    do sistema de dependências (Depends), a partir do Épico 1.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
