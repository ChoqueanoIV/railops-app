from sqlalchemy.orm import Session

from app.models.usuario import Usuario


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_matricula(self, matricula: str) -> Usuario | None:
        return (
            self.db.query(Usuario)
            .filter(Usuario.matricula == matricula)
            .first()
        )

    def criar(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def ativar_usuario(self, usuario: Usuario, novo_pin_hash: str) -> Usuario:
        usuario.senha_hash = novo_pin_hash
        usuario.pin_definido = True
        usuario.codigo_ativacao_hash = None
        self.db.commit()
        self.db.refresh(usuario)
        return usuario
