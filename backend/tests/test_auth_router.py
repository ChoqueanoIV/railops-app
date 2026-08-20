from unittest.mock import MagicMock

import pytest

from app.api.errors import ApiError
from app.routers import auth_router
from app.schemas.auth_schema import LoginRequest, PrimeiroAcessoRequest
from app.services.auth_service import AutenticacaoError


def test_primeiro_acesso_retorna_status_sem_expor_usuario(monkeypatch):
    ativar = MagicMock()
    monkeypatch.setattr(auth_router.AuthService, "primeiro_acesso", ativar)
    dados = PrimeiroAcessoRequest(
        matricula="30032552", codigo_ativacao="123456", pin="4321"
    )

    resposta = auth_router.primeiro_acesso(dados, MagicMock())

    assert resposta == {"mensagem": "PIN definido com sucesso"}
    ativar.assert_called_once_with("30032552", "123456", "4321")


def test_primeiro_acesso_converte_erro_de_negocio_em_400(monkeypatch):
    monkeypatch.setattr(
        auth_router.AuthService,
        "primeiro_acesso",
        MagicMock(side_effect=AutenticacaoError("Dados de ativação inválidos.")),
    )

    with pytest.raises(ApiError) as erro:
        auth_router.primeiro_acesso(
            PrimeiroAcessoRequest(
                matricula="30032552", codigo_ativacao="123456", pin="4321"
            ),
            MagicMock(),
        )

    assert erro.value.status_code == 400
    assert erro.value.code == "INVALID_ACTIVATION_DATA"
    assert erro.value.message == "Dados de ativação inválidos."


def test_login_retorna_token_bearer(monkeypatch):
    monkeypatch.setattr(
        auth_router.AuthService,
        "login",
        MagicMock(return_value="jwt-de-caracterizacao"),
    )

    resposta = auth_router.login(
        LoginRequest(matricula="30032552", pin="4321"), MagicMock()
    )

    assert resposta.access_token == "jwt-de-caracterizacao"
    assert resposta.token_type == "bearer"


def test_login_converte_erro_de_credencial_em_401(monkeypatch):
    monkeypatch.setattr(
        auth_router.AuthService,
        "login",
        MagicMock(side_effect=AutenticacaoError("Matrícula ou PIN inválidos.")),
    )

    with pytest.raises(ApiError) as erro:
        auth_router.login(LoginRequest(matricula="30032552", pin="4321"), MagicMock())

    assert erro.value.status_code == 401
    assert erro.value.code == "INVALID_CREDENTIALS"
    assert erro.value.message == "Matrícula ou PIN inválidos."
