import uuid
from datetime import date, datetime
from unittest.mock import MagicMock
from zoneinfo import ZoneInfo

import pytest
from tests.test_passagem_tecon_schema import LINHAS_TECON, dados_tecon_validos

from app.features.auth.models import Usuario
from app.features.passagens.exceptions import PassagemError
from app.features.passagens.models import (
    LadoLinha,
    Linha,
    PassagemLinhaOcupacao,
    PassagemServico,
    PassagemTeconDetalhe,
    Radio,
    Terminal,
    Turma,
    Turno,
)
from app.features.passagens.schemas import (
    PassagemTeconEdicaoRequest,
    PassagemTeconRequest,
)
from app.features.passagens.service import PassagemService


def criar_linhas_tecon() -> list[Linha]:
    return [
        Linha(
            id=uuid.uuid4(),
            terminal=Terminal.TECON,
            codigo=codigo,
            permite_sup_inf=False,
        )
        for codigo in LINHAS_TECON
    ]


def criar_service_tecon():
    passagem_repository = MagicMock()
    linha_repository = MagicMock()
    radio_repository = MagicMock()
    linha_repository.listar_por_terminal.return_value = criar_linhas_tecon()
    radio_repository.buscar_ou_criar.return_value = Radio(
        id=uuid.uuid4(), numero="R-TECON-01"
    )
    passagem_repository.salvar.side_effect = lambda passagem: passagem
    service = PassagemService(passagem_repository, linha_repository, radio_repository)
    return service, passagem_repository, linha_repository, radio_repository


def criar_dados_tecon_request() -> PassagemTeconRequest:
    dados = dados_tecon_validos()
    dados["equipe"] = [{"nome": "Operador TECON", "matricula": "12345678"}]
    dados["radios_utilizados"] = [
        {
            "numero": "R-TECON-01",
            "manobrador_nome": "Operador TECON",
            "apresentou_falha": False,
        }
    ]
    return PassagemTeconRequest(**dados)


def test_criar_tecon_sem_atendimento_monta_passagem_completa():
    service, passagem_repository, linha_repository, radio_repository = (
        criar_service_tecon()
    )
    responsavel = Usuario(id=uuid.uuid4(), matricula="30032552", nome="Responsável")

    passagem = service.criar_tecon(criar_dados_tecon_request(), responsavel)

    assert passagem.terminal == Terminal.TECON
    assert passagem.responsavel_id == responsavel.id
    assert passagem.detalhe_tecon.houve_atendimento is False
    assert len(passagem.ocupacoes_linhas) == 9
    assert len(passagem.equipe) == 1
    assert len(passagem.radios_utilizados) == 1
    linha_repository.listar_por_terminal.assert_called_once_with(Terminal.TECON)
    radio_repository.buscar_ou_criar.assert_called_once_with("R-TECON-01")
    passagem_repository.salvar.assert_called_once_with(passagem)


def test_criar_tecon_com_atendimento_preserva_areas_independentes():
    service, passagem_repository, _, _ = criar_service_tecon()
    dados = dados_tecon_validos()
    dados["detalhe"] = {
        "houve_atendimento": True,
        "carga_mal_posicionada": False,
        "area1_atendida": True,
        "area1_inicio": "08:00",
        "area1_termino": "09:00",
        "area2_atendida": False,
    }

    passagem = service.criar_tecon(
        PassagemTeconRequest(**dados), Usuario(id=uuid.uuid4())
    )

    assert passagem.detalhe_tecon.area1_atendida is True
    assert passagem.detalhe_tecon.area2_atendida is False
    passagem_repository.salvar.assert_called_once_with(passagem)


def test_criar_tecon_rejeita_linha_ausente_antes_de_persistir():
    service, passagem_repository, _, radio_repository = criar_service_tecon()
    dados = criar_dados_tecon_request()
    dados.ocupacoes_linhas.pop()

    with pytest.raises(PassagemError, match="todas as linhas"):
        service.criar_tecon(dados, Usuario(id=uuid.uuid4()))

    radio_repository.buscar_ou_criar.assert_not_called()
    passagem_repository.salvar.assert_not_called()


def test_criar_tecon_rejeita_linha_duplicada():
    service, passagem_repository, _, _ = criar_service_tecon()
    dados = criar_dados_tecon_request()
    dados.ocupacoes_linhas[-1].codigo_linha = "L1"

    with pytest.raises(PassagemError, match="uma única vez"):
        service.criar_tecon(dados, Usuario(id=uuid.uuid4()))

    passagem_repository.salvar.assert_not_called()


def test_criar_tecon_rejeita_sup_inf():
    service, passagem_repository, _, _ = criar_service_tecon()
    dados = criar_dados_tecon_request()
    dados.ocupacoes_linhas[0].sup_inf = LadoLinha.SUP

    with pytest.raises(PassagemError, match="não permitem"):
        service.criar_tecon(dados, Usuario(id=uuid.uuid4()))

    passagem_repository.salvar.assert_not_called()


def test_editar_tecon_preserva_identidade_e_confirma_snapshot():
    service, repository, _, _ = criar_service_tecon()
    responsavel = Usuario(id=uuid.uuid4())
    passagem = PassagemServico(
        id=uuid.uuid4(),
        terminal=Terminal.TECON,
        data=date(2026, 8, 14),
        turma=Turma.C,
        turno=Turno.NOTURNO,
        responsavel_id=responsavel.id,
        observacoes="Anterior",
        mobile_utilizado=True,
        detalhe_tecon=PassagemTeconDetalhe(houve_atendimento=False),
        ocupacoes_linhas=[
            PassagemLinhaOcupacao(linha=linha, veiculos="Anterior")
            for linha in criar_linhas_tecon()
        ],
    )
    repository.buscar_para_edicao.return_value = passagem
    repository.confirmar_edicao.side_effect = lambda registro: registro
    dados = dados_tecon_validos()
    for campo in ("data", "turma", "turno"):
        dados.pop(campo)
    dados["observacoes"] = "Atualizada"

    resultado = service.editar_tecon(
        passagem.id,
        PassagemTeconEdicaoRequest(**dados),
        responsavel,
        datetime(2026, 8, 14, 23, 0, tzinfo=ZoneInfo("America/Sao_Paulo")),
    )

    assert resultado.observacoes == "Atualizada"
    assert resultado.terminal == Terminal.TECON
    assert resultado.data == date(2026, 8, 14)
    repository.registrar_snapshot.assert_called_once_with(passagem, responsavel.id)
    repository.confirmar_edicao.assert_called_once_with(passagem)


def test_editar_tecon_rejeita_passagem_de_outro_terminal_e_desfaz():
    service, repository, _, _ = criar_service_tecon()
    responsavel = Usuario(id=uuid.uuid4())
    passagem = PassagemServico(
        id=uuid.uuid4(),
        terminal=Terminal.BRISAMAR,
        data=date(2026, 8, 14),
        turma=Turma.C,
        turno=Turno.NOTURNO,
        responsavel_id=responsavel.id,
        mobile_utilizado=True,
    )
    repository.buscar_para_edicao.return_value = passagem
    dados = dados_tecon_validos()
    for campo in ("data", "turma", "turno"):
        dados.pop(campo)

    with pytest.raises(PassagemError, match="não correspondem"):
        service.editar_tecon(
            passagem.id,
            PassagemTeconEdicaoRequest(**dados),
            responsavel,
            datetime(2026, 8, 14, 23, 0, tzinfo=ZoneInfo("America/Sao_Paulo")),
        )

    repository.registrar_snapshot.assert_not_called()
    repository.confirmar_edicao.assert_not_called()
    repository.desfazer.assert_called_once_with()
