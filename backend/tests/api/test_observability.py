import asyncio
import json
import re
from unittest.mock import MagicMock, patch

from fastapi import Request
from fastapi.responses import JSONResponse

from app.api.errors import tratar_erro_inesperado
from app.core.middleware import REQUEST_ID_HEADER, ObservabilidadeMiddleware


def criar_request(request_id: str | None = None, path: str = "/health") -> Request:
    headers = [] if request_id is None else [(b"x-request-id", request_id.encode())]
    return Request(
        {
            "type": "http",
            "method": "GET",
            "path": path,
            "root_path": "",
            "scheme": "http",
            "query_string": b"",
            "headers": headers,
            "client": ("127.0.0.1", 12345),
            "server": ("testserver", 80),
        }
    )


async def resposta_ok(_request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok"})


def executar_middleware(request: Request) -> JSONResponse:
    middleware = ObservabilidadeMiddleware(MagicMock())
    resposta = asyncio.run(middleware.dispatch(request, resposta_ok))
    assert isinstance(resposta, JSONResponse)
    return resposta


def test_resposta_inclui_request_id_e_headers_defensivos():
    resposta = executar_middleware(criar_request("avaliacao-123"))

    assert resposta.status_code == 200
    assert resposta.headers[REQUEST_ID_HEADER] == "avaliacao-123"
    assert resposta.headers["X-Content-Type-Options"] == "nosniff"
    assert resposta.headers["X-Frame-Options"] == "DENY"
    assert resposta.headers["Referrer-Policy"] == "no-referrer"


def test_request_id_invalido_nao_e_refletido():
    resposta = executar_middleware(criar_request("id\nforjado"))

    assert resposta.headers[REQUEST_ID_HEADER] != "id\nforjado"
    assert re.fullmatch(
        r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
        resposta.headers[REQUEST_ID_HEADER],
    )


def test_erro_inesperado_tem_log_correlacionavel_e_response_seguro():
    segredo = "pin=4321 token=jwt-secreto"
    request = criar_request("erro-controlado", "/_falha-controlada")
    request.state.request_id = "erro-controlado"

    with patch("app.api.errors.logger.exception") as registrar_erro:
        resposta = asyncio.run(tratar_erro_inesperado(request, RuntimeError(segredo)))

    assert resposta.status_code == 500
    assert resposta.headers[REQUEST_ID_HEADER] == "erro-controlado"
    assert resposta.headers["X-Content-Type-Options"] == "nosniff"
    assert resposta.headers["X-Frame-Options"] == "DENY"
    assert resposta.headers["Referrer-Policy"] == "no-referrer"
    assert json.loads(resposta.body) == {
        "detail": "Erro interno do servidor.",
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "Erro interno do servidor.",
            "details": None,
        },
    }
    registrar_erro.assert_called_once()
    assert segredo not in json.dumps(registrar_erro.call_args.args)
    assert segredo not in json.dumps(registrar_erro.call_args.kwargs, default=str)
