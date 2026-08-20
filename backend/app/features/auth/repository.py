import uuid

from sqlalchemy.orm import Session

from app.features.auth.models import Usuario
from app.shared.persistence.transactions import Transacao, TransacaoSQLAlchemy


class UsuarioRepository:
    def __init__(self, db: Session, transacao: Transacao | None = None):
        self.db = db
        self.transacao = transacao or TransacaoSQLAlchemy(db)

    def buscar_por_matricula(self, matricula: str) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.matricula == matricula).first()

    def buscar_por_id(self, usuario_id: uuid.UUID) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def criar(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.transacao.confirmar()
        self.transacao.atualizar(usuario)
        return usuario

    def ativar_usuario(self, usuario: Usuario, novo_pin_hash: str) -> Usuario:
        usuario.senha_hash = novo_pin_hash
        usuario.pin_definido = True
        usuario.codigo_ativacao_hash = None
        self.transacao.confirmar()
        self.transacao.atualizar(usuario)
        return usuario
