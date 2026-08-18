from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Configuracao, obter_configuracao
from app.routers.auth_router import router as auth_router
from app.routers.passagem_router import router as passagem_router


def health_check() -> dict[str, str]:
    return {"status": "ok"}


def criar_app(configuracao: Configuracao | None = None) -> FastAPI:
    configuracao_ativa = configuracao or obter_configuracao()
    aplicacao = FastAPI(title=configuracao_ativa.titulo_api)

    aplicacao.add_middleware(
        CORSMiddleware,
        allow_origins=list(configuracao_ativa.cors_origins),
        allow_methods=["*"],
        allow_headers=["*"],
    )

    aplicacao.include_router(auth_router)
    aplicacao.include_router(passagem_router)
    aplicacao.add_api_route(
        "/health",
        health_check,
        methods=["GET"],
        tags=["Infraestrutura"],
    )
    return aplicacao


app = criar_app()
