from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.api.errors import ApiError
from app.core.database import get_db
from app.features.auth.exceptions import AutenticacaoError
from app.features.auth.models import PerfilUsuario, Usuario
from app.features.auth.repository import UsuarioRepository
from app.features.auth.service import AuthService

bearer_scheme = HTTPBearer(auto_error=False)


def obter_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UsuarioRepository(db))


def obter_usuario_atual(
    credenciais: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    if credenciais is None:
        raise ApiError(
            status_code=401,
            code="NOT_AUTHENTICATED",
            message="Não autenticado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    service = obter_auth_service(db)

    try:
        return service.validar_token(credenciais.credentials)
    except AutenticacaoError:
        raise ApiError(
            status_code=401,
            code="NOT_AUTHENTICATED",
            message="Não autenticado.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None


def exigir_consulta_historico(
    usuario_atual: Usuario = Depends(obter_usuario_atual),
) -> Usuario:
    if usuario_atual.perfil not in {
        PerfilUsuario.INSTRUTOR,
        PerfilUsuario.MONITOR_QUALIDADE,
    }:
        raise ApiError(
            status_code=403,
            code="HISTORY_ACCESS_DENIED",
            message="Usuário sem permissão para consultar o histórico.",
        )
    return usuario_atual
