from main import app

ENDPOINTS_PUBLICOS = {
    "/health": {"get"},
    "/ready": {"get"},
    "/auth/primeiro-acesso": {"post"},
    "/auth/login": {"post"},
    "/passagens/brisamar": {"post"},
    "/passagens/tecon": {"post"},
    "/passagens/{passagem_id}": {"get", "put"},
}


def test_openapi_mantem_inventario_de_endpoints_publicos():
    caminhos = app.openapi()["paths"]

    assert set(caminhos) == set(ENDPOINTS_PUBLICOS)
    for caminho, metodos in ENDPOINTS_PUBLICOS.items():
        assert set(caminhos[caminho]) == metodos


def test_openapi_mantem_status_de_sucesso_atual():
    caminhos = app.openapi()["paths"]

    assert "200" in caminhos["/health"]["get"]["responses"]
    assert "200" in caminhos["/ready"]["get"]["responses"]
    assert "503" in caminhos["/ready"]["get"]["responses"]
    assert "201" in caminhos["/auth/primeiro-acesso"]["post"]["responses"]
    assert "200" in caminhos["/auth/login"]["post"]["responses"]
    assert "201" in caminhos["/passagens/brisamar"]["post"]["responses"]
    assert "201" in caminhos["/passagens/tecon"]["post"]["responses"]
    assert "200" in caminhos["/passagens/{passagem_id}"]["get"]["responses"]
    assert "200" in caminhos["/passagens/{passagem_id}"]["put"]["responses"]


def test_openapi_mantem_autenticacao_apenas_nas_rotas_de_passagem():
    caminhos = app.openapi()["paths"]

    assert caminhos["/health"]["get"].get("security") is None
    assert caminhos["/ready"]["get"].get("security") is None
    assert caminhos["/auth/login"]["post"].get("security") is None
    assert caminhos["/auth/primeiro-acesso"]["post"].get("security") is None
    for caminho in (
        "/passagens/brisamar",
        "/passagens/tecon",
        "/passagens/{passagem_id}",
    ):
        for operacao in caminhos[caminho].values():
            assert operacao["security"] == [{"HTTPBearer": []}]


def test_openapi_documenta_erros_conhecidos_com_schema_unico():
    caminhos = app.openapi()["paths"]

    respostas_esperadas = {
        ("/auth/primeiro-acesso", "post"): {"400"},
        ("/auth/login", "post"): {"401"},
        ("/passagens/brisamar", "post"): {"400", "401"},
        ("/passagens/tecon", "post"): {"400", "401"},
        ("/passagens/{passagem_id}", "get"): {"401", "404"},
        ("/passagens/{passagem_id}", "put"): {"400", "401"},
    }

    for (caminho, metodo), status_esperados in respostas_esperadas.items():
        respostas = caminhos[caminho][metodo]["responses"]
        assert status_esperados <= set(respostas)
        for status in status_esperados:
            schema = respostas[status]["content"]["application/json"]["schema"]
            assert schema["$ref"].endswith("/ErrorResponse")
