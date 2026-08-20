"""Adaptador temporário; use app.features.auth.dependencies."""

from app.features.auth.dependencies import (
    bearer_scheme,
    obter_auth_service,
    obter_usuario_atual,
)

__all__ = ["bearer_scheme", "obter_auth_service", "obter_usuario_atual"]
