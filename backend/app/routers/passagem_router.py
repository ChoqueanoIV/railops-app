import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.usuario import Usuario
from app.repositories.passagem_repository import (
    LinhaRepository,
    PassagemRepository,
    RadioRepository,
)
from app.routers.dependencies import obter_usuario_atual
from app.schemas.passagem_schema import (
    PassagemAtualizadaResponse,
    PassagemBrisamarEdicaoRequest,
    PassagemBrisamarRequest,
    PassagemCriadaResponse,
    PassagemTeconEdicaoRequest,
    PassagemTeconRequest,
)
from app.services.passagem_service import PassagemError, PassagemService


router = APIRouter(prefix="/passagens", tags=["Passagens de serviço"])


@router.post(
    "/brisamar",
    response_model=PassagemCriadaResponse,
    status_code=201,
)
def criar_passagem_brisamar(
    dados: PassagemBrisamarRequest,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    service = PassagemService(
        PassagemRepository(db),
        LinhaRepository(db),
        RadioRepository(db),
    )

    try:
        passagem = service.criar_brisamar(dados, usuario_atual)
    except PassagemError as erro:
        raise HTTPException(status_code=400, detail=str(erro))

    return PassagemCriadaResponse(
        id=passagem.id,
        mensagem="Passagem de serviço registrada com sucesso.",
    )


@router.post(
    "/tecon",
    response_model=PassagemCriadaResponse,
    status_code=201,
)
def criar_passagem_tecon(
    dados: PassagemTeconRequest,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    service = PassagemService(
        PassagemRepository(db),
        LinhaRepository(db),
        RadioRepository(db),
    )

    try:
        passagem = service.criar_tecon(dados, usuario_atual)
    except PassagemError as erro:
        raise HTTPException(status_code=400, detail=str(erro))

    return PassagemCriadaResponse(
        id=passagem.id,
        mensagem="Passagem de serviço registrada com sucesso.",
    )


@router.put("/{passagem_id}", response_model=PassagemAtualizadaResponse)
def editar_passagem(
    passagem_id: uuid.UUID,
    dados: PassagemBrisamarEdicaoRequest | PassagemTeconEdicaoRequest,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    service = PassagemService(
        PassagemRepository(db),
        LinhaRepository(db),
        RadioRepository(db),
    )

    try:
        if isinstance(dados, PassagemBrisamarEdicaoRequest):
            passagem = service.editar_brisamar(passagem_id, dados, usuario_atual)
        else:
            passagem = service.editar_tecon(passagem_id, dados, usuario_atual)
    except PassagemError as erro:
        raise HTTPException(status_code=400, detail=str(erro))

    return PassagemAtualizadaResponse(
        id=passagem.id,
        mensagem="Passagem de serviço atualizada com sucesso.",
    )
