from collections.abc import Mapping

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: object | None = None


class ErrorResponse(BaseModel):
    # Compatibilidade temporária com o frontend legado e clientes atuais.
    detail: object
    error: ErrorDetail


class ApiError(Exception):
    def __init__(
        self,
        *,
        status_code: int,
        code: str,
        message: str,
        details: object | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details
        self.headers = dict(headers) if headers is not None else None


def _conteudo_erro(
    *, code: str, message: str, details: object | None, legacy_detail: object
) -> dict[str, object]:
    return {
        "detail": legacy_detail,
        "error": {"code": code, "message": message, "details": details},
    }


async def tratar_api_error(_request: Request, erro: Exception) -> JSONResponse:
    assert isinstance(erro, ApiError)
    return JSONResponse(
        status_code=erro.status_code,
        content=_conteudo_erro(
            code=erro.code,
            message=erro.message,
            details=erro.details,
            legacy_detail=erro.message,
        ),
        headers=erro.headers,
    )


async def tratar_validacao(
    _request: Request, erro: Exception
) -> JSONResponse:
    assert isinstance(erro, RequestValidationError)
    detalhes = erro.errors()
    return JSONResponse(
        status_code=422,
        content=_conteudo_erro(
            code="REQUEST_VALIDATION_ERROR",
            message="Dados da requisição inválidos.",
            details=detalhes,
            legacy_detail=detalhes,
        ),
    )


async def tratar_http_exception(_request: Request, erro: Exception) -> JSONResponse:
    assert isinstance(erro, HTTPException)
    mensagem = erro.detail if isinstance(erro.detail, str) else "Requisição inválida."
    return JSONResponse(
        status_code=erro.status_code,
        content=_conteudo_erro(
            code="HTTP_ERROR",
            message=mensagem,
            details=None if isinstance(erro.detail, str) else erro.detail,
            legacy_detail=erro.detail,
        ),
        headers=erro.headers,
    )


def registrar_exception_handlers(aplicacao: FastAPI) -> None:
    aplicacao.add_exception_handler(ApiError, tratar_api_error)
    aplicacao.add_exception_handler(RequestValidationError, tratar_validacao)
    aplicacao.add_exception_handler(HTTPException, tratar_http_exception)


def resposta_erro(descricao: str) -> dict[str, object]:
    return {"model": ErrorResponse, "description": descricao}
