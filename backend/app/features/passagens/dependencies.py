from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.passagens.repository import (
    LinhaRepository,
    PassagemRepository,
    RadioRepository,
)
from app.features.passagens.service import PassagemCicloService, PassagemService


def obter_passagem_service(db: Session = Depends(get_db)) -> PassagemService:
    return PassagemService(
        PassagemRepository(db),
        LinhaRepository(db),
        RadioRepository(db),
    )


def obter_ciclo_service(db: Session = Depends(get_db)) -> PassagemCicloService:
    return PassagemCicloService(PassagemRepository(db))
