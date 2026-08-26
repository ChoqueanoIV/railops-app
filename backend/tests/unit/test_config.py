import pytest

from app.core.config import (
    ARQUIVO_ENV,
    PASTA_BACKEND,
    AmbienteAplicacao,
    Configuracao,
    obter_variavel_obrigatoria,
)


def test_arquivo_env_fica_na_raiz_do_backend():
    assert PASTA_BACKEND.name == "backend"
    assert ARQUIVO_ENV == PASTA_BACKEND / ".env"
    assert ARQUIVO_ENV.is_absolute()


def test_variavel_obrigatoria_rejeita_ausencia():
    with pytest.raises(RuntimeError, match="VARIAVEL_TESTE_AUSENTE"):
        obter_variavel_obrigatoria("VARIAVEL_TESTE_AUSENTE", {})


def test_variavel_obrigatoria_rejeita_valor_vazio():
    with pytest.raises(RuntimeError, match="VARIAVEL_TESTE_VAZIA"):
        obter_variavel_obrigatoria(
            "VARIAVEL_TESTE_VAZIA", {"VARIAVEL_TESTE_VAZIA": " "}
        )


def test_variavel_obrigatoria_retorna_valor_configurado():
    assert (
        obter_variavel_obrigatoria("VARIAVEL_TESTE", {"VARIAVEL_TESTE": " valor "})
        == "valor"
    )


def test_configuracao_carrega_valores_tipados_sem_credenciais_reais():
    configuracao = Configuracao.carregar(
        {
            "DATABASE_URL": "postgresql://teste:teste@localhost/teste",
            "JWT_SECRET_KEY": "segredo-de-teste",
            "RAILOPS_ENV": "test",
            "API_TITLE": "RailOps Teste",
            "CORS_ORIGINS": "http://localhost:3000, http://localhost:5173",
        }
    )

    assert configuracao.ambiente is AmbienteAplicacao.TESTE
    assert configuracao.titulo_api == "RailOps Teste"
    assert configuracao.cors_origins == (
        "http://localhost:3000",
        "http://localhost:5173",
    )


def test_configuracao_rejeita_ambiente_invalido():
    with pytest.raises(RuntimeError, match="RAILOPS_ENV inválido"):
        Configuracao.carregar(
            {
                "DATABASE_URL": "postgresql://teste:teste@localhost/teste",
                "JWT_SECRET_KEY": "segredo-de-teste",
                "RAILOPS_ENV": "homologacao-invalida",
            }
        )


def test_configuracao_rejeita_lista_cors_vazia():
    with pytest.raises(RuntimeError, match="CORS_ORIGINS"):
        Configuracao.carregar(
            {
                "DATABASE_URL": "postgresql://teste:teste@localhost/teste",
                "JWT_SECRET_KEY": "segredo-de-teste",
                "CORS_ORIGINS": " , ",
            }
        )


def test_producao_exige_segredo_jwt_com_ao_menos_32_bytes():
    with pytest.raises(RuntimeError, match="32 bytes"):
        Configuracao.carregar(
            {
                "DATABASE_URL": "postgresql://localhost/railops",
                "JWT_SECRET_KEY": "curto",
                "RAILOPS_ENV": "production",
                "CORS_ORIGINS": "https://railops.example",
            }
        )


def test_producao_rejeita_cors_aberto_para_qualquer_origem():
    with pytest.raises(RuntimeError, match="não permite"):
        Configuracao.carregar(
            {
                "DATABASE_URL": "postgresql://localhost/railops",
                "JWT_SECRET_KEY": "s" * 32,
                "RAILOPS_ENV": "production",
                "CORS_ORIGINS": "*",
            }
        )
