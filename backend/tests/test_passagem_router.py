import uuid
from unittest.mock import MagicMock

import pytest
from tests.test_passagem_repository import criar_passagem_completa_para_snapshot
from tests.test_passagem_service import criar_dados_edicao_brisamar, criar_dados_validos
from tests.test_passagem_tecon_service import criar_dados_tecon_request

from app.api.errors import ApiError
from app.features.auth.models import Usuario
from app.features.passagens import controller as passagem_controller
from app.features.passagens.exceptions import PassagemError
from app.features.passagens.models import PassagemTeconDetalhe, Terminal
from app.features.passagens.schemas import PassagemTeconEdicaoRequest


def test_criar_passagem_brisamar_retorna_id_e_mensagem(monkeypatch):
    passagem_id = uuid.uuid4()
    passagem = MagicMock(id=passagem_id)
    criar = MagicMock(return_value=passagem)
    monkeypatch.setattr(
        passagem_controller.PassagemService,
        "criar_brisamar",
        criar,
    )
    usuario = Usuario(id=uuid.uuid4())

    resposta = passagem_controller.criar_passagem_brisamar(
        criar_dados_validos(),
        criar_service(),
        usuario,
    )

    assert resposta.id == passagem_id
    assert resposta.mensagem == "Passagem de serviço registrada com sucesso."
    criar.assert_called_once()
    assert criar.call_args.args[1] is usuario


def test_criar_passagem_brisamar_converte_erro_de_negocio(monkeypatch):
    monkeypatch.setattr(
        passagem_controller.PassagemService,
        "criar_brisamar",
        MagicMock(side_effect=PassagemError("Dados inválidos.")),
    )

    with pytest.raises(ApiError) as erro:
        passagem_controller.criar_passagem_brisamar(
            criar_dados_validos(),
            criar_service(),
            Usuario(id=uuid.uuid4()),
        )

    assert erro.value.status_code == 400
    assert erro.value.code == "PASSAGEM_INVALID"
    assert erro.value.message == "Dados inválidos."


def test_criar_passagem_tecon_retorna_id_e_mensagem(monkeypatch):
    passagem_id = uuid.uuid4()
    passagem = MagicMock(id=passagem_id)
    criar = MagicMock(return_value=passagem)
    monkeypatch.setattr(
        passagem_controller.PassagemService,
        "criar_tecon",
        criar,
    )
    usuario = Usuario(id=uuid.uuid4())

    resposta = passagem_controller.criar_passagem_tecon(
        criar_dados_tecon_request(),
        criar_service(),
        usuario,
    )

    assert resposta.id == passagem_id
    assert resposta.mensagem == "Passagem de serviço registrada com sucesso."
    criar.assert_called_once()
    assert criar.call_args.args[1] is usuario


def test_criar_passagem_tecon_converte_erro_de_negocio(monkeypatch):
    monkeypatch.setattr(
        passagem_controller.PassagemService,
        "criar_tecon",
        MagicMock(side_effect=PassagemError("Dados do TECON inválidos.")),
    )

    with pytest.raises(ApiError) as erro:
        passagem_controller.criar_passagem_tecon(
            criar_dados_tecon_request(),
            criar_service(),
            Usuario(id=uuid.uuid4()),
        )

    assert erro.value.status_code == 400
    assert erro.value.code == "PASSAGEM_INVALID"
    assert erro.value.message == "Dados do TECON inválidos."


def test_editar_passagem_brisamar_retorna_id_e_mensagem(monkeypatch):
    passagem_id = uuid.uuid4()
    editar = MagicMock(return_value=MagicMock(id=passagem_id))
    monkeypatch.setattr(passagem_controller.PassagemService, "editar_brisamar", editar)
    dados = criar_dados_edicao_brisamar()
    usuario = Usuario(id=uuid.uuid4())

    resposta = passagem_controller.editar_passagem(
        passagem_id, dados, criar_service(), usuario
    )

    assert resposta.id == passagem_id
    assert resposta.mensagem == "Passagem de serviço atualizada com sucesso."
    editar.assert_called_once_with(passagem_id, dados, usuario)


def test_editar_passagem_tecon_encaminha_schema_correto(monkeypatch):
    passagem_id = uuid.uuid4()
    editar = MagicMock(return_value=MagicMock(id=passagem_id))
    monkeypatch.setattr(passagem_controller.PassagemService, "editar_tecon", editar)
    dados = criar_dados_tecon_request().model_dump()
    for campo in ("data", "turma", "turno"):
        dados.pop(campo)
    schema = PassagemTeconEdicaoRequest(**dados)
    usuario = Usuario(id=uuid.uuid4())

    passagem_controller.editar_passagem(passagem_id, schema, criar_service(), usuario)

    editar.assert_called_once_with(passagem_id, schema, usuario)


def test_editar_passagem_converte_erro_de_negocio(monkeypatch):
    monkeypatch.setattr(
        passagem_controller.PassagemService,
        "editar_brisamar",
        MagicMock(side_effect=PassagemError("Turno encerrado.")),
    )

    with pytest.raises(ApiError) as erro:
        passagem_controller.editar_passagem(
            uuid.uuid4(),
            criar_dados_edicao_brisamar(),
            criar_service(),
            Usuario(id=uuid.uuid4()),
        )

    assert erro.value.status_code == 400
    assert erro.value.code == "PASSAGEM_UPDATE_INVALID"
    assert erro.value.message == "Turno encerrado."


def test_consultar_passagem_retorna_detalhes_e_permissao(monkeypatch):
    passagem = criar_passagem_completa_para_snapshot()
    monkeypatch.setattr(
        passagem_controller.PassagemService,
        "obter_por_id",
        MagicMock(return_value=passagem),
    )
    monkeypatch.setattr(
        passagem_controller.PassagemService,
        "passagem_editavel",
        MagicMock(return_value=True),
    )

    resposta = passagem_controller.consultar_passagem(
        passagem.id, criar_service(), Usuario(id=passagem.responsavel_id)
    )

    assert resposta.id == passagem.id
    assert resposta.editavel is True
    assert resposta.detalhe.radios_operantes == 4
    assert resposta.ocupacoes_linhas[0].codigo_linha == "22"
    assert resposta.radios_utilizados[0].numero == "R-01"


def test_montar_resposta_consulta_preserva_detalhe_tecon():
    passagem = criar_passagem_completa_para_snapshot()
    passagem.terminal = Terminal.TECON
    passagem.detalhe_brisamar = None
    passagem.detalhe_tecon = PassagemTeconDetalhe(
        houve_atendimento=False,
        carga_mal_posicionada=None,
        area1_atendida=None,
        area2_atendida=None,
    )

    resposta = passagem_controller.montar_resposta_consulta(passagem, False)

    assert resposta.terminal == Terminal.TECON
    assert resposta.detalhe.houve_atendimento is False
    assert resposta.editavel is False


def test_consultar_passagem_inexistente_retorna_404(monkeypatch):
    monkeypatch.setattr(
        passagem_controller.PassagemService,
        "obter_por_id",
        MagicMock(side_effect=PassagemError("Passagem de serviço não encontrada.")),
    )

    with pytest.raises(ApiError) as erro:
        passagem_controller.consultar_passagem(
            uuid.uuid4(), criar_service(), Usuario(id=uuid.uuid4())
        )

    assert erro.value.status_code == 404
    assert erro.value.code == "PASSAGEM_NOT_FOUND"


def criar_service() -> passagem_controller.PassagemService:
    return passagem_controller.PassagemService(MagicMock(), MagicMock(), MagicMock())
