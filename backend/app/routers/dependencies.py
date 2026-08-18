from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.services.auth_service import AutenticacaoError, AuthService

bearer_scheme = HTTPBearer(auto_error=False)


def obter_usuario_atual(
    credenciais: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    if credenciais is None:
        raise HTTPException(
            status_code=401,
            detail="Não autenticado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    repository = UsuarioRepository(db)
    service = AuthService(repository)

    try:
        return service.validar_token(credenciais.credentials)
    except AutenticacaoError:
        raise HTTPException(
            status_code=401,
            detail="Não autenticado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
