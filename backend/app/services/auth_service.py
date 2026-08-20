"""Adaptador temporário; use app.features.auth.service."""

from app.features.auth.exceptions import AutenticacaoError
from app.features.auth.service import (
    ALGORITHM,
    EXPIRACAO_TOKEN_MINUTOS,
    SECRET_KEY,
    AuthService,
    pwd_context,
)

__all__ = [
    "ALGORITHM",
    "EXPIRACAO_TOKEN_MINUTOS",
    "SECRET_KEY",
    "AuthService",
    "AutenticacaoError",
    "pwd_context",
]
