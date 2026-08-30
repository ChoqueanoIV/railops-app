import uuid
from datetime import date, datetime
from unittest.mock import MagicMock
from zoneinfo import ZoneInfo

import pytest

from app.features.auth.models import Usuario
from app.features.passagens.exceptions import PassagemError
from app.features.passagens.models import (
    CicloPassagem,
    EquipeMembro,
    EstadoCicloPassagem,
    LadoLinha,
    Linha,
    PassagemBrisamarDetalhe,
    PassagemLinhaOcupacao,
    PassagemServico,
    Radio,
    Terminal,
    Turma,
    Turno,
)
from app.features.passagens.schemas import (
    PassagemBrisamarEdicaoRequest,
    PassagemBrisamarRequest,
)
from app.features.passagens.service import PassagemService

CODIGOS_BRISAMAR = [
    "16",
    "18",
    "20",
    "22 SUP",
    "22 INF",
    "Travessão L22",
    "24 SUP",
    "24 INF",
    "Travessão L24",
    "26",
    "28",
    "30",
]


def criar_linhas_brisamar() -> list[Linha]:
    return [
        Linha(
            id=uuid.uuid4(),
            terminal=Terminal.BRISAMAR,
            codigo=codigo,
            permite_sup_inf=False,
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
                "sup_inf": None,
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
    passagem_repository.obter_ou_criar_ciclo.side_effect = (
        lambda data, turma, turno, criado_por: CicloPassagem(
            data=data,
            turma=turma,
            turno=turno,
            estado=EstadoCicloPassagem.RASCUNHO,
            criado_por=criado_por,
            passagens=[],
        )
    )
    service = PassagemService(passagem_repository, linha_repository, radio_repository)
    return service, passagem_repository, linha_repository, radio_repository


def test_criar_brisamar_monta_passagem_completa():
    service, passagem_repository, linha_repository, radio_repository = criar_service()
    responsavel = Usuario(id=uuid.uuid4(), matricula="30032552", nome="Responsável")

    passagem = service.criar_brisamar(criar_dados_validos(), responsavel)

    assert passagem.terminal == Terminal.BRISAMAR
    assert passagem.ciclo is not None
    assert passagem.ciclo.estado == EstadoCicloPassagem.RASCUNHO
    assert passagem.responsavel_id == responsavel.id
    assert len(passagem.ocupacoes_linhas) == 12
    assert len(passagem.equipe) == 1
    assert len(passagem.radios_utilizados) == 1
    assert passagem.detalhe_brisamar.radios_operantes == 4
    linha_repository.listar_por_terminal.assert_called_once_with(Terminal.BRISAMAR)
    radio_repository.buscar_ou_criar.assert_called_once_with("R-01")
    passagem_repository.salvar.assert_called_once_with(passagem)


def test_criar_brisamar_rejeita_terminal_duplicado_no_mesmo_ciclo():
    service, passagem_repository, _, _ = criar_service()
    responsavel = Usuario(id=uuid.uuid4())
    ciclo = CicloPassagem(
        data=date(2026, 8, 13),
        turma=Turma.A,
        turno=Turno.DIURNO,
        criado_por=responsavel.id,
        passagens=[PassagemServico(terminal=Terminal.BRISAMAR)],
    )
    passagem_repository.obter_ou_criar_ciclo.return_value = ciclo
    passagem_repository.obter_ou_criar_ciclo.side_effect = None

    with pytest.raises(PassagemError, match="BRISAMAR já foi preenchido"):
        service.criar_brisamar(criar_dados_validos(), responsavel)

    passagem_repository.salvar.assert_not_called()


def test_criar_brisamar_aceita_lados_e_travessoes_como_ocupacoes_independentes():
    service, passagem_repository, linha_repository, _ = criar_service()
    linhas = [
        Linha(
            id=uuid.uuid4(),
            terminal=Terminal.BRISAMAR,
            codigo=codigo,
            permite_sup_inf=False,
        )
        for codigo in CODIGOS_BRISAMAR
    ]
    linha_repository.listar_por_terminal.return_value = linhas
    dados = criar_dados_validos().model_dump()
    dados["ocupacoes_linhas"] = [
        {"codigo_linha": codigo, "veiculos": f"Ocupação {codigo}"}
        for codigo in CODIGOS_BRISAMAR
    ]

    passagem = service.criar_brisamar(
        PassagemBrisamarRequest(**dados), Usuario(id=uuid.uuid4())
    )

    assert [item.linha.codigo for item in passagem.ocupacoes_linhas] == (
        CODIGOS_BRISAMAR
    )
    assert all(item.sup_inf is None for item in passagem.ocupacoes_linhas)
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


def test_criar_brisamar_rejeita_formato_antigo_exclusivo_da_linha_22():
    service, passagem_repository, _, _ = criar_service()
    dados = criar_dados_validos()
    ocupacao_22_sup = next(
        item for item in dados.ocupacoes_linhas if item.codigo_linha == "22 SUP"
    )
    ocupacao_22_sup.codigo_linha = "22"
    ocupacao_22_sup.sup_inf = LadoLinha.SUP

    with pytest.raises(PassagemError, match="todas as linhas"):
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


def test_consulta_por_id_retorna_passagem_sem_validar_autoria():
    service, repository, _, _ = criar_service()
    passagem = criar_passagem_para_edicao(Turno.DIURNO)
    repository.buscar_por_id.return_value = passagem

    assert service.obter_por_id(passagem.id) is passagem


def test_consulta_por_id_rejeita_registro_inexistente():
    service, repository, _, _ = criar_service()
    repository.buscar_por_id.return_value = None

    with pytest.raises(PassagemError, match="não encontrada"):
        service.obter_por_id(uuid.uuid4())


def criar_dados_edicao_brisamar() -> PassagemBrisamarEdicaoRequest:
    dados = criar_dados_validos().model_dump()
    dados.pop("data")
    dados.pop("turma")
    dados.pop("turno")
    dados["observacoes"] = "Estado atualizado"
    return PassagemBrisamarEdicaoRequest(**dados)


def criar_passagem_brisamar_existente(responsavel_id) -> PassagemServico:
    linhas = criar_linhas_brisamar()
    return PassagemServico(
        id=uuid.uuid4(),
        terminal=Terminal.BRISAMAR,
        data=date(2026, 8, 14),
        turma=Turma.C,
        turno=Turno.DIURNO,
        responsavel_id=responsavel_id,
        observacoes="Estado anterior",
        mobile_utilizado=True,
        detalhe_brisamar=PassagemBrisamarDetalhe(
            radios_operantes=2,
            radios_inoperantes=0,
            baterias=2,
            carregadores=1,
        ),
        equipe=[EquipeMembro(nome="Antigo", matricula="87654321")],
        ocupacoes_linhas=[
            PassagemLinhaOcupacao(linha=linha, veiculos="Anterior") for linha in linhas
        ],
    )


def test_editar_brisamar_registra_estado_anterior_e_confirma_uma_vez():
    service, repository, _, _ = criar_service()
    responsavel = Usuario(id=uuid.uuid4())
    passagem = criar_passagem_brisamar_existente(responsavel.id)
    repository.buscar_para_edicao.return_value = passagem
    repository.confirmar_edicao.side_effect = lambda registro: registro
    estado_no_snapshot = []
    repository.registrar_snapshot.side_effect = lambda registro, _: (
        estado_no_snapshot.append(registro.observacoes)
    )
    detalhe_anterior = passagem.detalhe_brisamar
    ocupacoes_anteriores = list(passagem.ocupacoes_linhas)

    resultado = service.editar_brisamar(
        passagem.id,
        criar_dados_edicao_brisamar(),
        responsavel,
        datetime(2026, 8, 14, 12, 0, tzinfo=FUSO_SP),
    )

    assert resultado.observacoes == "Estado atualizado"
    assert estado_no_snapshot == ["Estado anterior"]
    assert resultado.data == date(2026, 8, 14)
    assert resultado.turma == Turma.C
    assert resultado.turno == Turno.DIURNO
    assert resultado.equipe[0].nome == "Operador"
    assert resultado.detalhe_brisamar is detalhe_anterior
    assert resultado.detalhe_brisamar.radios_operantes == 4
    assert all(
        atual is anterior
        for atual, anterior in zip(resultado.ocupacoes_linhas, ocupacoes_anteriores)
    )
    repository.registrar_snapshot.assert_called_once_with(passagem, responsavel.id)
    repository.confirmar_edicao.assert_called_once_with(passagem)
    repository.desfazer.assert_not_called()


def test_editar_brisamar_desfaz_sem_snapshot_quando_linhas_sao_invalidas():
    service, repository, _, _ = criar_service()
    responsavel = Usuario(id=uuid.uuid4())
    passagem = criar_passagem_brisamar_existente(responsavel.id)
    repository.buscar_para_edicao.return_value = passagem
    dados = criar_dados_edicao_brisamar()
    dados.ocupacoes_linhas.pop()

    with pytest.raises(PassagemError, match="todas as linhas"):
        service.editar_brisamar(
            passagem.id,
            dados,
            responsavel,
            datetime(2026, 8, 14, 12, 0, tzinfo=FUSO_SP),
        )

    repository.registrar_snapshot.assert_not_called()
    repository.confirmar_edicao.assert_not_called()
    repository.desfazer.assert_called_once_with()


def test_editar_brisamar_desfaz_snapshot_se_mutacao_falha():
    service, repository, _, radio_repository = criar_service()
    responsavel = Usuario(id=uuid.uuid4())
    passagem = criar_passagem_brisamar_existente(responsavel.id)
    repository.buscar_para_edicao.return_value = passagem
    radio_repository.buscar_ou_criar.side_effect = RuntimeError("falha simulada")

    with pytest.raises(RuntimeError, match="falha simulada"):
        service.editar_brisamar(
            passagem.id,
            criar_dados_edicao_brisamar(),
            responsavel,
            datetime(2026, 8, 14, 12, 0, tzinfo=FUSO_SP),
        )

    repository.registrar_snapshot.assert_called_once()
    repository.confirmar_edicao.assert_not_called()
    repository.desfazer.assert_called_once_with()
