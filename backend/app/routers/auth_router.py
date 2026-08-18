from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.auth_schema import LoginRequest, LoginResponse, PrimeiroAcessoRequest
from app.services.auth_service import AutenticacaoError, AuthService

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/primeiro-acesso", status_code=201)
def primeiro_acesso(dados: PrimeiroAcessoRequest, db: Session = Depends(get_db)):
    repository = UsuarioRepository(db)
    service = AuthService(repository)
    try:
        service.primeiro_acesso(dados.matricula, dados.codigo_ativacao, dados.pin)
    except AutenticacaoError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    return {"mensagem": "PIN definido com sucesso"}


@router.post("/login", response_model=LoginResponse)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    repository = UsuarioRepository(db)
    service = AuthService(repository)
    try:
        token = service.login(dados.matricula, dados.pin)
    except AutenticacaoError as erro:
        raise HTTPException(status_code=401, detail=str(erro))
    return LoginResponse(access_token=token)
