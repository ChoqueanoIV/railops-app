"""Adaptador temporário; use app.features.auth.schemas."""

from app.features.auth.schemas import LoginRequest, LoginResponse, PrimeiroAcessoRequest

__all__ = ["LoginRequest", "LoginResponse", "PrimeiroAcessoRequest"]
