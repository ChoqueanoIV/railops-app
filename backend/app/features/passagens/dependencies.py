from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.passagens.repository import (
    LinhaRepository,
    PassagemRepository,
    RadioRepository,
)
from app.features.passagens.service import PassagemService


def obter_passagem_service(db: Session = Depends(get_db)) -> PassagemService:
    return PassagemService(
        PassagemRepository(db),
        LinhaRepository(db),
        RadioRepository(db),
    )
