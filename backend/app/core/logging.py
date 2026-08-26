import json
import logging
from datetime import datetime, timezone
from typing import Final

LOGGER_NAME: Final = "railops"
_HANDLER_MARKER: Final = "_railops_json_handler"


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        conteudo: dict[str, object] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "event": record.getMessage(),
        }
        for campo in (
            "request_id",
            "method",
            "path",
            "status_code",
            "duration_ms",
        ):
            valor = getattr(record, campo, None)
            if valor is not None:
                conteudo[campo] = valor
        if record.exc_info and record.exc_info[0] is not None:
            conteudo["exception"] = record.exc_info[0].__name__
        return json.dumps(conteudo, ensure_ascii=False)


def configurar_logging() -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    if not any(getattr(handler, _HANDLER_MARKER, False) for handler in logger.handlers):
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        setattr(handler, _HANDLER_MARKER, True)
        logger.addHandler(handler)
    logger.propagate = False
    return logger


def obter_logger(nome: str) -> logging.Logger:
    return logging.getLogger(f"{LOGGER_NAME}.{nome}")
