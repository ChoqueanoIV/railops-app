"""Adaptador temporário; use app.features.auth.dependencies."""

from app.features.auth.dependencies import bearer_scheme, obter_usuario_atual

__all__ = ["bearer_scheme", "obter_usuario_atual"]
