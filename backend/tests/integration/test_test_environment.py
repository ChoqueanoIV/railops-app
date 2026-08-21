def test_banco_configurado_para_suite_nao_aponta_para_producao(
    banco_teste_url: str,
) -> None:
    assert banco_teste_url.endswith("/railops_test")
