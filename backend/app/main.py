import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.api.errors import registrar_exception_handlers
from app.core.config import Configuracao, obter_configuracao
from app.core.database import engine
from app.core.logging import configurar_logging
from app.core.middleware import REQUEST_ID_HEADER, ObservabilidadeMiddleware
from app.features.auth.controller import router as auth_router
from app.features.passagens.controller import router as passagem_router


def health_check() -> dict[str, str]:
    return {"status": "ok"}


def readiness_check() -> dict[str, str] | JSONResponse:
    try:
        with engine.connect() as conexao:
            conexao.execute(text("SELECT 1"))
    except SQLAlchemyError:
        logging.getLogger("railops.readiness").warning("database_unavailable")
        return JSONResponse(status_code=503, content={"status": "unavailable"})
    return {"status": "ok"}


def criar_app(configuracao: Configuracao | None = None) -> FastAPI:
    configuracao_ativa = configuracao or obter_configuracao()
    configurar_logging()
    aplicacao = FastAPI(title=configuracao_ativa.titulo_api)
    registrar_exception_handlers(aplicacao)

    aplicacao.add_middleware(
        CORSMiddleware,
        allow_origins=list(configuracao_ativa.cors_origins),
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=[REQUEST_ID_HEADER, "Content-Disposition"],
    )
    aplicacao.add_middleware(ObservabilidadeMiddleware)

    aplicacao.include_router(auth_router)
    aplicacao.include_router(passagem_router)
    aplicacao.add_api_route(
        "/health",
        health_check,
        methods=["GET"],
        tags=["Infraestrutura"],
    )
    aplicacao.add_api_route(
        "/ready",
        readiness_check,
        methods=["GET"],
        tags=["Infraestrutura"],
        response_model=None,
        responses={503: {"description": "Banco de dados indisponível"}},
    )
    return aplicacao


app = criar_app()
