import uuid
from typing import Protocol

from app.features.auth.models import Usuario


class UsuarioRepositoryProtocol(Protocol):
    def buscar_por_matricula(self, matricula: str) -> Usuario | None: ...

    def buscar_por_id(self, usuario_id: uuid.UUID) -> Usuario | None: ...

    def ativar_usuario(self, usuario: Usuario, novo_pin_hash: str) -> Usuario: ...
