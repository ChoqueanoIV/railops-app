import json
import logging

from app.core.logging import JsonFormatter, configurar_logging


def test_formatter_json_registra_apenas_campos_operacionais_permitidos():
    registro = logging.LogRecord(
        name="railops.http",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="request_completed",
        args=(),
        exc_info=None,
    )
    registro.request_id = "req-123"
    registro.method = "GET"
    registro.path = "/health"
    registro.status_code = 200
    registro.authorization = "Bearer jwt-secreto"

    conteudo = json.loads(JsonFormatter().format(registro))

    assert conteudo["event"] == "request_completed"
    assert conteudo["request_id"] == "req-123"
    assert conteudo["status_code"] == 200
    assert "authorization" not in conteudo
    assert "jwt-secreto" not in json.dumps(conteudo)


def test_configuracao_de_logging_e_idempotente():
    logger = configurar_logging()
    quantidade_inicial = len(logger.handlers)

    configurar_logging()

    assert len(logger.handlers) == quantidade_inicial
