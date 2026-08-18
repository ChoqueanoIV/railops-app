from main import health_check


def test_health_check_informa_que_api_esta_ativa():
    assert health_check() == {"status": "ok"}
