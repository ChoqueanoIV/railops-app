import pytest
from fastapi import FastAPI

from app.core.config import AmbienteAplicacao, Configuracao
from app.main import criar_app


@pytest.fixture
def configuracao_teste() -> Configuracao:
    return Configuracao(
        database_url="postgresql://railops_test:railops_test@localhost/railops_test",
        jwt_secret_key="segredo-ficticio-exclusivo-para-testes",
        ambiente=AmbienteAplicacao.TESTE,
        titulo_api="RailOps Teste",
        cors_origins=("http://localhost:5173",),
    )


@pytest.fixture
def app_teste(configuracao_teste: Configuracao) -> FastAPI:
    return criar_app(configuracao_teste)
