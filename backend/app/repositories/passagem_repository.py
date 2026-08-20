"""Adaptador temporário; use app.features.passagens.repository."""

from app.features.passagens.repository import (
    LinhaRepository,
    PassagemRepository,
    RadioRepository,
)

__all__ = ["LinhaRepository", "PassagemRepository", "RadioRepository"]
