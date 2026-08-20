from typing import Protocol

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


class PersistenciaError(Exception):
    """Falha de infraestrutura sem detalhes internos do banco."""


class Transacao(Protocol):
    def confirmar(self) -> None: ...

    def desfazer(self) -> None: ...

    def atualizar(self, registro: object) -> None: ...


class TransacaoSQLAlchemy:
    def __init__(self, db: Session) -> None:
        self.db = db

    def confirmar(self) -> None:
        try:
            self.db.commit()
        except SQLAlchemyError as erro:
            self.db.rollback()
            raise PersistenciaError(
                "Não foi possível concluir a operação no banco de dados."
            ) from erro

    def desfazer(self) -> None:
        self.db.rollback()

    def atualizar(self, registro: object) -> None:
        try:
            self.db.refresh(registro)
        except SQLAlchemyError as erro:
            self.db.rollback()
            raise PersistenciaError(
                "Não foi possível atualizar o estado persistido."
            ) from erro
