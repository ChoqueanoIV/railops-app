import uuid
from unittest.mock import MagicMock

import pytest

from app.models.passagem import LadoLinha, Linha, Radio, Terminal
from app.models.usuario import Usuario
from app.schemas.passagem_schema import PassagemBrisamarRequest
from app.services.passagem_service import PassagemError, PassagemService


CODIGOS_BRISAMAR = ["16", "18", "20", "22", "24", "26", "28", "30"]


def criar_linhas_brisamar() -> list[Linha]:
    return [
        Linha(
            id=uuid.uuid4(),
            terminal=Terminal.BRISAMAR,
            codigo=codigo,
            permite_sup_inf=codigo in {"22", "24"},
        )
        for codigo in CODIGOS_BRISAMAR
    ]


def criar_dados_validos() -> PassagemBrisamarRequest:
    return PassagemBrisamarRequest(
        data="2026-08-13",
        turno="A",
        observacoes="Sem alterações",
        relatorio_ocorrencias="Sem ocorrências",
        mobile_utilizado=True,
        equipe=[{"nome": "Operador", "matricula": "12345678"}],
        ocupacoes_linhas=[
            {
                "codigo_linha": codigo,
                "veiculos": "Livre",
                "sup_inf": "SUP" if codigo in {"22", "24"} else None,
            }
            for codigo in CODIGOS_BRISAMAR
        ],
        detalhe={
            "radios_operantes": 4,
            "radios_inoperantes": 1,
            "baterias": 5,
            "carregadores": 2,
        },
        radios_utilizados=[
            {
                "numero": "R-01",
                "manobrador_nome": "Operador",
                "apresentou_falha": False,
            }
        ],
    )


def criar_service():
    passagem_repository = MagicMock()
    linha_repository = MagicMock()
    radio_repository = MagicMock()
    linha_repository.listar_por_terminal.return_value = criar_linhas_brisamar()
    radio_repository.buscar_ou_criar.return_value = Radio(
        id=uuid.uuid4(), numero="R-01"
    )
    passagem_repository.salvar.side_effect = lambda passagem: passagem
    service = PassagemService(
        passagem_repository, linha_repository, radio_repository
    )
    return service, passagem_repository, linha_repository, radio_repository


def test_criar_brisamar_monta_passagem_completa():
    service, passagem_repository, linha_repository, radio_repository = (
        criar_service()
    )
    responsavel = Usuario(id=uuid.uuid4(), matricula="30032552", nome="Responsável")

    passagem = service.criar_brisamar(criar_dados_validos(), responsavel)

    assert passagem.terminal == Terminal.BRISAMAR
    assert passagem.responsavel_id == responsavel.id
    assert len(passagem.ocupacoes_linhas) == 8
    assert len(passagem.equipe) == 1
    assert len(passagem.radios_utilizados) == 1
    assert passagem.detalhe_brisamar.radios_operantes == 4
    linha_repository.listar_por_terminal.assert_called_once_with(Terminal.BRISAMAR)
    radio_repository.buscar_ou_criar.assert_called_once_with("R-01")
    passagem_repository.salvar.assert_called_once_with(passagem)


def test_criar_brisamar_rejeita_linha_ausente_antes_de_persistir():
    service, passagem_repository, _, radio_repository = criar_service()
    dados = criar_dados_validos()
    dados.ocupacoes_linhas.pop()

    with pytest.raises(PassagemError, match="todas as linhas"):
        service.criar_brisamar(dados, Usuario(id=uuid.uuid4()))

    radio_repository.buscar_ou_criar.assert_not_called()
    passagem_repository.salvar.assert_not_called()


def test_criar_brisamar_rejeita_linha_duplicada():
    service, passagem_repository, _, _ = criar_service()
    dados = criar_dados_validos()
    dados.ocupacoes_linhas[-1].codigo_linha = "16"

    with pytest.raises(PassagemError, match="uma única vez"):
        service.criar_brisamar(dados, Usuario(id=uuid.uuid4()))

    passagem_repository.salvar.assert_not_called()


def test_criar_brisamar_exige_sup_inf_na_linha_22():
    service, passagem_repository, _, _ = criar_service()
    dados = criar_dados_validos()
    ocupacao_22 = next(
        item for item in dados.ocupacoes_linhas if item.codigo_linha == "22"
    )
    ocupacao_22.sup_inf = None

    with pytest.raises(PassagemError, match="linha 22 exige"):
        service.criar_brisamar(dados, Usuario(id=uuid.uuid4()))

    passagem_repository.salvar.assert_not_called()


def test_criar_brisamar_rejeita_sup_inf_na_linha_16():
    service, passagem_repository, _, _ = criar_service()
    dados = criar_dados_validos()
    ocupacao_16 = next(
        item for item in dados.ocupacoes_linhas if item.codigo_linha == "16"
    )
    ocupacao_16.sup_inf = LadoLinha.INF

    with pytest.raises(PassagemError, match="linha 16 não permite"):
        service.criar_brisamar(dados, Usuario(id=uuid.uuid4()))

    passagem_repository.salvar.assert_not_called()
