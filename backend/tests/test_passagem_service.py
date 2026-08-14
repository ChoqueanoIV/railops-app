import uuid
from datetime import date, datetime
from unittest.mock import MagicMock
from zoneinfo import ZoneInfo

import pytest

from app.models.passagem import (
    LadoLinha,
    Linha,
    PassagemServico,
    Radio,
    Terminal,
    Turma,
    Turno,
)
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
        turma="A",
        turno="DIURNO",
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


FUSO_SP = ZoneInfo("America/Sao_Paulo")


def criar_passagem_para_edicao(turno: Turno, responsavel_id=None):
    return PassagemServico(
        id=uuid.uuid4(),
        data=date(2026, 8, 14),
        turma=Turma.C,
        turno=turno,
        responsavel_id=responsavel_id or uuid.uuid4(),
    )


@pytest.mark.parametrize(
    ("turno", "momento"),
    (
        (Turno.DIURNO, datetime(2026, 8, 14, 7, 0, tzinfo=FUSO_SP)),
        (Turno.DIURNO, datetime(2026, 8, 14, 18, 59, tzinfo=FUSO_SP)),
        (Turno.NOTURNO, datetime(2026, 8, 14, 19, 0, tzinfo=FUSO_SP)),
        (Turno.NOTURNO, datetime(2026, 8, 15, 6, 59, tzinfo=FUSO_SP)),
    ),
)
def test_edicao_permitida_durante_o_proprio_turno(turno, momento):
    responsavel = Usuario(id=uuid.uuid4())
    passagem = criar_passagem_para_edicao(turno, responsavel.id)

    PassagemService.validar_permissao_edicao(passagem, responsavel, momento)


@pytest.mark.parametrize(
    ("turno", "momento"),
    (
        (Turno.DIURNO, datetime(2026, 8, 14, 6, 59, tzinfo=FUSO_SP)),
        (Turno.DIURNO, datetime(2026, 8, 14, 19, 0, tzinfo=FUSO_SP)),
        (Turno.NOTURNO, datetime(2026, 8, 14, 18, 59, tzinfo=FUSO_SP)),
        (Turno.NOTURNO, datetime(2026, 8, 15, 7, 0, tzinfo=FUSO_SP)),
    ),
)
def test_edicao_bloqueada_fora_do_proprio_turno(turno, momento):
    responsavel = Usuario(id=uuid.uuid4())
    passagem = criar_passagem_para_edicao(turno, responsavel.id)

    with pytest.raises(PassagemError, match="turno estiver em andamento"):
        PassagemService.validar_permissao_edicao(passagem, responsavel, momento)


def test_edicao_bloqueada_para_usuario_diferente_do_autor():
    passagem = criar_passagem_para_edicao(Turno.DIURNO)

    with pytest.raises(PassagemError, match="Somente o autor"):
        PassagemService.validar_permissao_edicao(
            passagem,
            Usuario(id=uuid.uuid4()),
            datetime(2026, 8, 14, 18, 50, tzinfo=FUSO_SP),
        )


def test_edicao_bloqueada_para_registro_legado_sem_turma_e_turno():
    responsavel = Usuario(id=uuid.uuid4())
    passagem = PassagemServico(
        id=uuid.uuid4(),
        data=date(2026, 8, 14),
        turno_legado="TESTE-E2E",
        responsavel_id=responsavel.id,
    )

    with pytest.raises(PassagemError, match="anterior à separação"):
        PassagemService.validar_permissao_edicao(
            passagem,
            responsavel,
            datetime(2026, 8, 14, 18, 50, tzinfo=FUSO_SP),
        )


def test_busca_para_edicao_desfaz_transacao_quando_validacao_falha():
    service, passagem_repository, _, _ = criar_service()
    passagem_repository.buscar_para_edicao.return_value = None

    with pytest.raises(PassagemError, match="não encontrada"):
        service.obter_para_edicao(uuid.uuid4(), Usuario(id=uuid.uuid4()))

    passagem_repository.desfazer.assert_called_once_with()
