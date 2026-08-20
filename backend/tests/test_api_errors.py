import asyncio
import json
from unittest.mock import MagicMock

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError

from app.api.errors import (
    ApiError,
    tratar_api_error,
    tratar_http_exception,
    tratar_validacao,
)


def conteudo_json(resposta) -> dict:
    return json.loads(resposta.body)


def test_erro_conhecido_tem_code_estavel_e_detail_compativel():
    erro = ApiError(
        status_code=409,
        code="KNOWN_CONFLICT",
        message="Conflito conhecido.",
        details={"campo": "valor"},
    )

    resposta = asyncio.run(tratar_api_error(MagicMock(), erro))

    assert resposta.status_code == 409
    assert conteudo_json(resposta) == {
        "detail": "Conflito conhecido.",
        "error": {
            "code": "KNOWN_CONFLICT",
            "message": "Conflito conhecido.",
            "details": {"campo": "valor"},
        },
    }


def test_erro_de_validacao_preserva_lista_em_detail():
    erro = RequestValidationError(
        [
            {
                "type": "int_parsing",
                "loc": ("path", "item_id"),
                "msg": "Input should be a valid integer",
                "input": "invalido",
            }
        ]
    )

    resposta = asyncio.run(tratar_validacao(MagicMock(), erro))
    conteudo = conteudo_json(resposta)

    assert resposta.status_code == 422
    assert isinstance(conteudo["detail"], list)
    assert conteudo["error"]["code"] == "REQUEST_VALIDATION_ERROR"
    assert conteudo["error"]["details"] == conteudo["detail"]


def test_http_exception_legada_recebe_envelope_sem_perder_detail():
    erro = HTTPException(status_code=403, detail="Acesso negado.")

    resposta = asyncio.run(tratar_http_exception(MagicMock(), erro))

    assert resposta.status_code == 403
    assert conteudo_json(resposta)["detail"] == "Acesso negado."
    assert conteudo_json(resposta)["error"] == {
        "code": "HTTP_ERROR",
        "message": "Acesso negado.",
        "details": None,
    }
