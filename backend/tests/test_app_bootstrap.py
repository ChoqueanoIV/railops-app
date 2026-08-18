from app.core.config import AmbienteAplicacao, Configuracao
from app.main import criar_app


def criar_configuracao_teste() -> Configuracao:
    return Configuracao(
        database_url="postgresql://teste:teste@localhost/teste",
        jwt_secret_key="segredo-de-teste",
        ambiente=AmbienteAplicacao.TESTE,
        titulo_api="RailOps Teste",
        cors_origins=("http://localhost:5173",),
    )


def test_criar_app_mantem_swagger_e_titulo_configurado():
    app = criar_app(criar_configuracao_teste())

    assert app.title == "RailOps Teste"
    assert app.docs_url == "/docs"
    assert app.openapi_url == "/openapi.json"


def test_criar_app_mantem_rotas_publicas_do_baseline():
    app = criar_app(criar_configuracao_teste())
    rotas = set(app.openapi()["paths"])

    assert "/health" in rotas
    assert "/auth/login" in rotas
    assert "/passagens/brisamar" in rotas
