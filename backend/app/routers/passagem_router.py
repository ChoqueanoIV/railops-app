"""Adaptador temporário; use app.features.passagens.controller."""

from app.features.passagens.controller import (
    consultar_passagem,
    criar_passagem_brisamar,
    criar_passagem_tecon,
    editar_passagem,
    montar_resposta_consulta,
    router,
)

__all__ = [
    "consultar_passagem",
    "criar_passagem_brisamar",
    "criar_passagem_tecon",
    "editar_passagem",
    "montar_resposta_consulta",
    "router",
]
