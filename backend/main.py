"""Entrypoint compatível para ``uvicorn main:app`` durante a migração."""

from app.main import app, criar_app, health_check

__all__ = ["app", "criar_app", "health_check"]
