import pytest

from app.core.config import ARQUIVO_ENV, PASTA_BACKEND, obter_variavel_obrigatoria


def test_arquivo_env_fica_na_raiz_do_backend():
    assert PASTA_BACKEND.name == "backend"
    assert ARQUIVO_ENV == PASTA_BACKEND / ".env"
    assert ARQUIVO_ENV.is_absolute()


def test_variavel_obrigatoria_rejeita_ausencia(monkeypatch):
    monkeypatch.delenv("VARIAVEL_TESTE_AUSENTE", raising=False)

    with pytest.raises(RuntimeError, match="VARIAVEL_TESTE_AUSENTE"):
        obter_variavel_obrigatoria("VARIAVEL_TESTE_AUSENTE")


def test_variavel_obrigatoria_rejeita_valor_vazio(monkeypatch):
    monkeypatch.setenv("VARIAVEL_TESTE_VAZIA", "   ")

    with pytest.raises(RuntimeError, match="VARIAVEL_TESTE_VAZIA"):
        obter_variavel_obrigatoria("VARIAVEL_TESTE_VAZIA")


def test_variavel_obrigatoria_retorna_valor_configurado(monkeypatch):
    monkeypatch.setenv("VARIAVEL_TESTE", "valor-seguro")

    assert obter_variavel_obrigatoria("VARIAVEL_TESTE") == "valor-seguro"
