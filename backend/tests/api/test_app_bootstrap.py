from fastapi import FastAPI


def test_criar_app_mantem_swagger_e_titulo_configurado(app_teste: FastAPI):
    assert app_teste.title == "RailOps Teste"
    assert app_teste.docs_url == "/docs"
    assert app_teste.openapi_url == "/openapi.json"


def test_criar_app_mantem_rotas_publicas_do_baseline(app_teste: FastAPI):
    rotas = set(app_teste.openapi()["paths"])

    assert "/health" in rotas
    assert "/auth/login" in rotas
    assert "/passagens/brisamar" in rotas
