"""Adaptador temporário; use app.features.auth.controller."""

from app.features.auth.controller import login, primeiro_acesso, router

__all__ = ["login", "primeiro_acesso", "router"]
