"""Adaptador temporário; use app.features.passagens.service."""

from app.features.passagens.exceptions import PassagemError
from app.features.passagens.service import FUSO_OPERACAO, PassagemService

__all__ = ["FUSO_OPERACAO", "PassagemError", "PassagemService"]
