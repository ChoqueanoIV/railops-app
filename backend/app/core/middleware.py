import re
import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import obter_logger

REQUEST_ID_HEADER = "X-Request-ID"
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
}
_REQUEST_ID_VALIDO = re.compile(r"^[A-Za-z0-9._-]{1,128}$")
logger = obter_logger("http")

CallNext = Callable[[Request], Awaitable[Response]]


def obter_request_id(valor_recebido: str | None) -> str:
    if valor_recebido and _REQUEST_ID_VALIDO.fullmatch(valor_recebido):
        return valor_recebido
    return str(uuid.uuid4())


class ObservabilidadeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: CallNext) -> Response:
        request_id = obter_request_id(request.headers.get(REQUEST_ID_HEADER))
        request.state.request_id = request_id
        inicio = time.perf_counter()

        response = await call_next(request)
        response.headers[REQUEST_ID_HEADER] = request_id
        response.headers.update(SECURITY_HEADERS)

        logger.info(
            "request_completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round((time.perf_counter() - inicio) * 1000, 2),
            },
        )
        return response
