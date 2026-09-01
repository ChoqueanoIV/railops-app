import uuid
from datetime import UTC, date, datetime
from unittest.mock import MagicMock

import pytest

from app.api.errors import ApiError
from app.features.auth.models import Usuario
from app.features.passagens import controller as passagem_controller
from app.features.passagens.exceptions import PassagemError
from app.features.passagens.models import (
    CicloPassagem,
    EstadoCicloPassagem,
    PassagemServico,
    PassagemServicoHistorico,
    PassagemTeconDetalhe,
    Terminal,
    Turma,
    Turno,
)
from app.features.passagens.schemas import (
    CicloConsultaFiltros,
    CicloPassagemResponse,
    PassagemTeconEdicaoRequest,
)
from tests.integration.test_passagem_repository import (
    criar_passagem_completa_para_snapshot,
)
from tests.unit.test_passagem_service import (
    criar_dados_edicao_brisamar,
    criar_dados_validos,
)
from tests.unit.test_passagem_tecon_service import criar_dados_tecon_request


def test_criar_passagem_brisamar_retorna_id_e_mensagem(monkeypatch):
    passagem_id = uuid.uuid4()
    ciclo = CicloPassagem(
        id=uuid.uuid4(), passagens=[PassagemServico(terminal=Terminal.BRISAMAR)]
    )
    passagem = MagicMock(id=passagem_id, ciclo_id=ciclo.id, ciclo=ciclo)
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
    ciclo = CicloPassagem(
        id=uuid.uuid4(), passagens=[PassagemServico(terminal=Terminal.TECON)]
    )
    passagem = MagicMock(id=passagem_id, ciclo_id=ciclo.id, ciclo=ciclo)
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


def test_consultar_historico_retorna_estado_atual_autor_e_paginacao(monkeypatch):
    passagem = criar_passagem_completa_para_snapshot()
    alterador = Usuario(nome="Instrutor", matricula="87654321")
    item = PassagemServicoHistorico(
        passagem_id=passagem.id,
        versao=2,
        snapshot={"passagem": {"observacoes": "Estado anterior"}},
        alterado_por=uuid.uuid4(),
        alterado_em=datetime(2026, 8, 30, 15, 45, tzinfo=UTC),
        alterador=alterador,
    )
    service = criar_service()
    monkeypatch.setattr(
        service,
        "consultar_historico",
        MagicMock(return_value=(passagem, [item], 21)),
    )
    monkeypatch.setattr(service, "passagem_editavel", MagicMock(return_value=False))

    resposta = passagem_controller.consultar_historico_passagem(
        passagem.id,
        pagina=2,
        por_pagina=20,
        service=service,
        usuario_atual=Usuario(id=uuid.uuid4()),
    )

    assert resposta.passagem_atual.id == passagem.id
    assert resposta.itens[0].versao == 2
    assert resposta.itens[0].alterador.matricula == "87654321"
    assert resposta.itens[0].snapshot["passagem"]["observacoes"] == "Estado anterior"
    assert resposta.paginacao.total_paginas == 2


def test_consultar_historico_inexistente_retorna_404(monkeypatch):
    service = criar_service()
    monkeypatch.setattr(
        service,
        "consultar_historico",
        MagicMock(side_effect=PassagemError("Passagem de serviço não encontrada.")),
    )

    with pytest.raises(ApiError) as erro:
        passagem_controller.consultar_historico_passagem(
            uuid.uuid4(),
            pagina=1,
            por_pagina=20,
            service=service,
            usuario_atual=Usuario(id=uuid.uuid4()),
        )

    assert erro.value.status_code == 404
    assert erro.value.code == "PASSAGEM_NOT_FOUND"


def test_listar_ciclos_retorna_responsavel_e_paginacao(monkeypatch):
    usuario = Usuario(id=uuid.uuid4(), nome="Responsável", matricula="30032552")
    ciclo = CicloPassagem(
        id=uuid.uuid4(),
        data=date(2026, 8, 30),
        turma=Turma.C,
        turno=Turno.DIURNO,
        estado=EstadoCicloPassagem.CONFIRMADO,
        criado_por=usuario.id,
        confirmado_em=datetime(2026, 8, 30, 18, 50, tzinfo=UTC),
        criador=usuario,
        passagens=[],
    )
    ciclo_service = passagem_controller.PassagemCicloService(MagicMock())
    monkeypatch.setattr(
        ciclo_service,
        "listar",
        MagicMock(return_value=([ciclo], 21, date(2026, 8, 1), date(2026, 8, 30))),
    )
    monkeypatch.setattr(
        passagem_controller,
        "montar_resposta_ciclo",
        MagicMock(
            return_value=CicloPassagemResponse(
                id=ciclo.id,
                data=ciclo.data,
                turma=ciclo.turma,
                turno=ciclo.turno,
                estado=ciclo.estado,
                confirmado_em=ciclo.confirmado_em,
                terminal_pendente=None,
                passagens=[],
            )
        ),
    )
    filtros = CicloConsultaFiltros(pagina=2, por_pagina=20)

    resposta = passagem_controller.listar_ciclos_confirmados(
        filtros, ciclo_service, criar_service(), usuario
    )

    assert resposta.itens[0].id == ciclo.id
    assert resposta.itens[0].responsavel.matricula == "30032552"
    assert resposta.paginacao.total_itens == 21
    assert resposta.paginacao.total_paginas == 2


def test_exportar_ciclo_pdf_retorna_download_autenticado(monkeypatch):
    usuario = Usuario(id=uuid.uuid4(), nome="Responsável", matricula="30032552")
    ciclo = CicloPassagem(
        id=uuid.uuid4(),
        data=date(2026, 8, 31),
        turma=Turma.C,
        turno=Turno.DIURNO,
        estado=EstadoCicloPassagem.CONFIRMADO,
        criado_por=usuario.id,
        confirmado_em=datetime(2026, 8, 31, 18, 45, tzinfo=UTC),
        criador=usuario,
        passagens=[criar_passagem_completa_para_snapshot()],
    )
    ciclo_service = passagem_controller.PassagemCicloService(MagicMock())
    monkeypatch.setattr(
        ciclo_service,
        "obter_confirmado_para_exportacao",
        MagicMock(return_value=ciclo),
    )

    resposta = passagem_controller.exportar_ciclo_pdf(ciclo.id, ciclo_service, usuario)

    assert resposta.media_type == "application/pdf"
    assert bytes(resposta.body).startswith(b"%PDF-")
    assert resposta.headers["content-disposition"] == (
        f'attachment; filename="railops-passagem-2026-08-31-{ciclo.id}.pdf"'
    )


def test_exportar_ciclos_csv_retorna_download_com_periodo(monkeypatch):
    ciclo = criar_ciclo_confirmado_para_exportacao()
    ciclo_service = passagem_controller.PassagemCicloService(MagicMock())
    monkeypatch.setattr(
        ciclo_service,
        "listar_para_exportacao",
        MagicMock(return_value=([ciclo], date(2026, 8, 1), date(2026, 8, 31))),
    )

    resposta = passagem_controller.exportar_ciclos_csv(
        CicloConsultaFiltros(), ciclo_service, ciclo.criador
    )

    assert resposta.media_type == "text/csv; charset=utf-8"
    assert bytes(resposta.body).startswith(b"\xef\xbb\xbfprotocolo,")
    assert resposta.headers["content-disposition"] == (
        'attachment; filename="railops-passagens-2026-08-01-2026-08-31.csv"'
    )


def test_exportar_ciclos_pdf_retorna_download_com_periodo(monkeypatch):
    ciclo = criar_ciclo_confirmado_para_exportacao()
    ciclo_service = passagem_controller.PassagemCicloService(MagicMock())
    monkeypatch.setattr(
        ciclo_service,
        "listar_para_exportacao",
        MagicMock(return_value=([ciclo], date(2026, 8, 1), date(2026, 8, 31))),
    )

    resposta = passagem_controller.exportar_ciclos_pdf(
        CicloConsultaFiltros(), ciclo_service, ciclo.criador
    )

    assert resposta.media_type == "application/pdf"
    assert bytes(resposta.body).startswith(b"%PDF-")
    assert resposta.headers["content-disposition"] == (
        'attachment; filename="railops-passagens-2026-08-01-2026-08-31.pdf"'
    )


def criar_ciclo_confirmado_para_exportacao() -> CicloPassagem:
    usuario = Usuario(id=uuid.uuid4(), nome="Responsável", matricula="30032552")
    return CicloPassagem(
        id=uuid.uuid4(),
        data=date(2026, 8, 31),
        turma=Turma.C,
        turno=Turno.DIURNO,
        estado=EstadoCicloPassagem.CONFIRMADO,
        criado_por=usuario.id,
        confirmado_em=datetime(2026, 8, 31, 18, 45, tzinfo=UTC),
        criador=usuario,
        passagens=[criar_passagem_completa_para_snapshot()],
    )


def criar_service() -> passagem_controller.PassagemService:
    return passagem_controller.PassagemService(MagicMock(), MagicMock(), MagicMock())
