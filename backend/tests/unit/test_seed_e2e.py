from unittest.mock import MagicMock

import pytest
from scripts import seed_e2e

from app.core.config import AmbienteAplicacao, Configuracao


def configuracao(ambiente: AmbienteAplicacao, url: str) -> Configuracao:
    return Configuracao(
        database_url=url,
        jwt_secret_key="segredo-de-teste",
        ambiente=ambiente,
    )


def test_seed_e2e_recusa_ambiente_fora_de_teste(monkeypatch):
    monkeypatch.setattr(
        seed_e2e,
        "obter_configuracao",
        MagicMock(
            return_value=configuracao(
                AmbienteAplicacao.DESENVOLVIMENTO,
                "postgresql://railops:senha@db:5432/railops_e2e",
            )
        ),
    )

    with pytest.raises(RuntimeError, match="RAILOPS_ENV=test"):
        seed_e2e.validar_destino()


@pytest.mark.parametrize(
    "url",
    [
        "postgresql://railops:senha@localhost:5432/railops_e2e",
        "postgresql://railops:senha@db:5432/railops",
    ],
)
def test_seed_e2e_recusa_banco_fora_do_compose_isolado(monkeypatch, url):
    monkeypatch.setattr(
        seed_e2e,
        "obter_configuracao",
        MagicMock(return_value=configuracao(AmbienteAplicacao.TESTE, url)),
    )

    with pytest.raises(RuntimeError, match="ambiente isolado"):
        seed_e2e.validar_destino()


def test_seed_e2e_aceita_somente_banco_interno_dedicado(monkeypatch):
    monkeypatch.setattr(
        seed_e2e,
        "obter_configuracao",
        MagicMock(
            return_value=configuracao(
                AmbienteAplicacao.TESTE,
                "postgresql://railops:senha@db:5432/railops_e2e",
            )
        ),
    )

    seed_e2e.validar_destino()
