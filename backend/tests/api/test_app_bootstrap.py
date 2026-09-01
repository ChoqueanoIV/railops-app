from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def test_criar_app_mantem_swagger_e_titulo_configurado(app_teste: FastAPI):
    assert app_teste.title == "RailOps Teste"
    assert app_teste.docs_url == "/docs"
    assert app_teste.openapi_url == "/openapi.json"


def test_criar_app_mantem_rotas_publicas_do_baseline(app_teste: FastAPI):
    rotas = set(app_teste.openapi()["paths"])

    assert "/health" in rotas
    assert "/ready" in rotas
    assert "/auth/login" in rotas
    assert "/passagens/brisamar" in rotas


def test_criar_app_expoe_nome_dos_downloads_ao_frontend(app_teste: FastAPI):
    cors = next(
        middleware
        for middleware in app_teste.user_middleware
        if middleware.cls is CORSMiddleware
    )

    assert "Content-Disposition" in cors.kwargs["expose_headers"]
