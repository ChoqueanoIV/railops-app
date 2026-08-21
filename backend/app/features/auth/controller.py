from fastapi import APIRouter, Depends

from app.api.errors import ApiError, resposta_erro
from app.features.auth.dependencies import obter_auth_service
from app.features.auth.exceptions import AutenticacaoError
from app.features.auth.schemas import (
    LoginRequest,
    LoginResponse,
    PrimeiroAcessoRequest,
)
from app.features.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post(
    "/primeiro-acesso",
    status_code=201,
    summary="Definir PIN no primeiro acesso",
    responses={400: resposta_erro("Dados de ativação inválidos")},
)
def primeiro_acesso(
    dados: PrimeiroAcessoRequest,
    service: AuthService = Depends(obter_auth_service),
) -> dict[str, str]:
    try:
        service.primeiro_acesso(dados.matricula, dados.codigo_ativacao, dados.pin)
    except AutenticacaoError as erro:
        raise ApiError(
            status_code=400,
            code="INVALID_ACTIVATION_DATA",
            message=str(erro),
        ) from erro
    return {"mensagem": "PIN definido com sucesso"}


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Autenticar usuário",
    responses={401: resposta_erro("Credenciais inválidas")},
)
def login(
    dados: LoginRequest,
    service: AuthService = Depends(obter_auth_service),
) -> LoginResponse:
    try:
        token = service.login(dados.matricula, dados.pin)
    except AutenticacaoError as erro:
        raise ApiError(
            status_code=401,
            code="INVALID_CREDENTIALS",
            message=str(erro),
        ) from erro
    return LoginResponse(access_token=token)
