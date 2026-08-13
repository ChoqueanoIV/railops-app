import uuid
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.models.usuario import Usuario
from app.routers import passagem_router
from app.services.passagem_service import PassagemError
from tests.test_passagem_service import criar_dados_validos


def test_criar_passagem_brisamar_retorna_id_e_mensagem(monkeypatch):
    passagem_id = uuid.uuid4()
    passagem = MagicMock(id=passagem_id)
    criar = MagicMock(return_value=passagem)
    monkeypatch.setattr(
        passagem_router.PassagemService,
        "criar_brisamar",
        criar,
    )
    usuario = Usuario(id=uuid.uuid4())

    resposta = passagem_router.criar_passagem_brisamar(
        criar_dados_validos(),
        MagicMock(),
        usuario,
    )

    assert resposta.id == passagem_id
    assert resposta.mensagem == "Passagem de serviço registrada com sucesso."
    criar.assert_called_once()
    assert criar.call_args.args[1] is usuario


def test_criar_passagem_brisamar_converte_erro_de_negocio(monkeypatch):
    monkeypatch.setattr(
        passagem_router.PassagemService,
        "criar_brisamar",
        MagicMock(side_effect=PassagemError("Dados inválidos.")),
    )

    with pytest.raises(HTTPException) as erro:
        passagem_router.criar_passagem_brisamar(
            criar_dados_validos(),
            MagicMock(),
            Usuario(id=uuid.uuid4()),
        )

    assert erro.value.status_code == 400
    assert erro.value.detail == "Dados inválidos."
