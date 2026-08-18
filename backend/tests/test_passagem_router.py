import uuid
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.models.usuario import Usuario
from app.routers import passagem_router
from app.schemas.passagem_schema import PassagemTeconEdicaoRequest
from app.services.passagem_service import PassagemError
from tests.test_passagem_service import criar_dados_edicao_brisamar, criar_dados_validos
from tests.test_passagem_repository import criar_passagem_completa_para_snapshot
from tests.test_passagem_tecon_service import criar_dados_tecon_request


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


def test_criar_passagem_tecon_retorna_id_e_mensagem(monkeypatch):
    passagem_id = uuid.uuid4()
    passagem = MagicMock(id=passagem_id)
    criar = MagicMock(return_value=passagem)
    monkeypatch.setattr(
        passagem_router.PassagemService,
        "criar_tecon",
        criar,
    )
    usuario = Usuario(id=uuid.uuid4())

    resposta = passagem_router.criar_passagem_tecon(
        criar_dados_tecon_request(),
        MagicMock(),
        usuario,
    )

    assert resposta.id == passagem_id
    assert resposta.mensagem == "Passagem de serviço registrada com sucesso."
    criar.assert_called_once()
    assert criar.call_args.args[1] is usuario


def test_criar_passagem_tecon_converte_erro_de_negocio(monkeypatch):
    monkeypatch.setattr(
        passagem_router.PassagemService,
        "criar_tecon",
        MagicMock(side_effect=PassagemError("Dados do TECON inválidos.")),
    )

    with pytest.raises(HTTPException) as erro:
        passagem_router.criar_passagem_tecon(
            criar_dados_tecon_request(),
            MagicMock(),
            Usuario(id=uuid.uuid4()),
        )

    assert erro.value.status_code == 400
    assert erro.value.detail == "Dados do TECON inválidos."


def test_editar_passagem_brisamar_retorna_id_e_mensagem(monkeypatch):
    passagem_id = uuid.uuid4()
    editar = MagicMock(return_value=MagicMock(id=passagem_id))
    monkeypatch.setattr(passagem_router.PassagemService, "editar_brisamar", editar)
    dados = criar_dados_edicao_brisamar()
    usuario = Usuario(id=uuid.uuid4())

    resposta = passagem_router.editar_passagem(
        passagem_id, dados, MagicMock(), usuario
    )

    assert resposta.id == passagem_id
    assert resposta.mensagem == "Passagem de serviço atualizada com sucesso."
    editar.assert_called_once_with(passagem_id, dados, usuario)


def test_editar_passagem_tecon_encaminha_schema_correto(monkeypatch):
    passagem_id = uuid.uuid4()
    editar = MagicMock(return_value=MagicMock(id=passagem_id))
    monkeypatch.setattr(passagem_router.PassagemService, "editar_tecon", editar)
    dados = criar_dados_tecon_request().model_dump()
    for campo in ("data", "turma", "turno"):
        dados.pop(campo)
    schema = PassagemTeconEdicaoRequest(**dados)
    usuario = Usuario(id=uuid.uuid4())

    passagem_router.editar_passagem(passagem_id, schema, MagicMock(), usuario)

    editar.assert_called_once_with(passagem_id, schema, usuario)


def test_editar_passagem_converte_erro_de_negocio(monkeypatch):
    monkeypatch.setattr(
        passagem_router.PassagemService,
        "editar_brisamar",
        MagicMock(side_effect=PassagemError("Turno encerrado.")),
    )

    with pytest.raises(HTTPException) as erro:
        passagem_router.editar_passagem(
            uuid.uuid4(),
            criar_dados_edicao_brisamar(),
            MagicMock(),
            Usuario(id=uuid.uuid4()),
        )

    assert erro.value.status_code == 400
    assert erro.value.detail == "Turno encerrado."


def test_consultar_passagem_retorna_detalhes_e_permissao(monkeypatch):
    passagem = criar_passagem_completa_para_snapshot()
    monkeypatch.setattr(
        passagem_router.PassagemService,
        "obter_por_id",
        MagicMock(return_value=passagem),
    )
    monkeypatch.setattr(
        passagem_router.PassagemService,
        "passagem_editavel",
        MagicMock(return_value=True),
    )

    resposta = passagem_router.consultar_passagem(
        passagem.id, MagicMock(), Usuario(id=passagem.responsavel_id)
    )

    assert resposta.id == passagem.id
    assert resposta.editavel is True
    assert resposta.detalhe.radios_operantes == 4
    assert resposta.ocupacoes_linhas[0].codigo_linha == "22"
    assert resposta.radios_utilizados[0].numero == "R-01"


def test_consultar_passagem_inexistente_retorna_404(monkeypatch):
    monkeypatch.setattr(
        passagem_router.PassagemService,
        "obter_por_id",
        MagicMock(side_effect=PassagemError("Passagem de serviço não encontrada.")),
    )

    with pytest.raises(HTTPException) as erro:
        passagem_router.consultar_passagem(
            uuid.uuid4(), MagicMock(), Usuario(id=uuid.uuid4())
        )

    assert erro.value.status_code == 404
