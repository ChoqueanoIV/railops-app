from unittest.mock import MagicMock, patch

from fastapi.responses import JSONResponse
from main import health_check, readiness_check
from sqlalchemy.exc import OperationalError


def test_health_check_informa_que_api_esta_ativa():
    assert health_check() == {"status": "ok"}


def test_readiness_informa_ok_sem_expor_dados_do_banco():
    conexao = MagicMock()
    with patch("app.main.engine.connect") as conectar:
        conectar.return_value.__enter__.return_value = conexao

        assert readiness_check() == {"status": "ok"}

    conexao.execute.assert_called_once()


def test_readiness_indisponivel_retorna_apenas_status_seguro():
    erro = OperationalError("SELECT 1", {}, RuntimeError("senha=secreta"))
    with patch("app.main.engine.connect", side_effect=erro):
        resposta = readiness_check()

    assert isinstance(resposta, JSONResponse)
    assert resposta.status_code == 503
    assert resposta.body == b'{"status":"unavailable"}'
