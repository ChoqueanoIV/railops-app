from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.api.errors import ApiError
from app.core.database import get_db
from app.features.auth.exceptions import AutenticacaoError
from app.features.auth.models import Usuario
from app.features.auth.repository import UsuarioRepository
from app.features.auth.service import AuthService

bearer_scheme = HTTPBearer(auto_error=False)


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

    repository = UsuarioRepository(db)
    service = AuthService(repository)

    try:
        return service.validar_token(credenciais.credentials)
    except AutenticacaoError:
        raise ApiError(
            status_code=401,
            code="NOT_AUTHENTICATED",
            message="Não autenticado.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None
