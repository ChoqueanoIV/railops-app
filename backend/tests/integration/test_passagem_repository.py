import json
import uuid
from datetime import date, time
from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.features.passagens.models import (
    CicloPassagem,
    EquipeMembro,
    Linha,
    PassagemBrisamarDetalhe,
    PassagemLinhaOcupacao,
    PassagemRadioUso,
    PassagemServico,
    PassagemServicoHistorico,
    Radio,
    Terminal,
    Turma,
    Turno,
)
from app.features.passagens.repository import (
    LinhaRepository,
    PassagemRepository,
    RadioRepository,
)
from app.shared.persistence.transactions import PersistenciaError


def test_linha_repository_lista_catalogo_ordenado_por_terminal():
    db = MagicMock()
    linhas = [Linha(codigo="16"), Linha(codigo="18")]
    consulta = db.query.return_value.filter.return_value.order_by.return_value
    consulta.all.return_value = linhas
    repository = LinhaRepository(db)

    resultado = repository.listar_por_terminal(Terminal.BRISAMAR)

    assert resultado == linhas
    db.query.assert_called_once_with(Linha)
    consulta.all.assert_called_once_with()


def test_radio_repository_reutiliza_radio_existente():
    db = MagicMock()
    radio_existente = Radio(numero="R-01")
    db.query.return_value.filter.return_value.first.return_value = radio_existente
    repository = RadioRepository(db)

    resultado = repository.buscar_ou_criar("R-01")

    assert resultado is radio_existente
    db.add.assert_not_called()
    db.flush.assert_not_called()


def test_radio_repository_adiciona_sem_commit():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None
    repository = RadioRepository(db)

    resultado = repository.buscar_ou_criar("R-02")

    assert resultado.numero == "R-02"
    db.add.assert_called_once_with(resultado)
    db.flush.assert_called_once_with()
    db.commit.assert_not_called()


def test_passagem_repository_confirma_transacao_completa():
    db = MagicMock()
    repository = PassagemRepository(db)
    passagem = PassagemServico()

    resultado = repository.salvar(passagem)

    assert resultado is passagem
    db.add.assert_called_once_with(passagem)
    db.commit.assert_called_once_with()
    db.refresh.assert_called_once_with(passagem)
    db.rollback.assert_not_called()


def test_passagem_repository_bloqueia_ciclo_antes_da_confirmacao():
    db = MagicMock()
    consulta = db.query.return_value.options.return_value.filter.return_value
    ciclo = CicloPassagem(id=uuid.uuid4())
    consulta.with_for_update.return_value.first.return_value = ciclo
    repository = PassagemRepository(db)

    resultado = repository.buscar_ciclo_para_confirmacao(ciclo.id)

    assert resultado is ciclo
    db.query.assert_called_once_with(CicloPassagem)
    consulta.with_for_update.assert_called_once_with()


def test_passagem_repository_serializa_criacao_da_mesma_identidade():
    db = MagicMock()
    consulta = db.query.return_value.options.return_value.filter.return_value
    consulta.with_for_update.return_value.first.return_value = None
    repository = PassagemRepository(db)
    criado_por = uuid.uuid4()

    ciclo = repository.obter_ou_criar_ciclo(
        date(2026, 8, 30), Turma.C, Turno.NOTURNO, criado_por
    )

    comando = str(db.execute.call_args.args[0])
    assert "pg_advisory_xact_lock" in comando
    assert db.execute.call_args.args[1] == {"identidade": "2026-08-30|C|NOTURNO"}
    assert ciclo.criado_por == criado_por
    db.add.assert_called_once_with(ciclo)
    db.flush.assert_called_once_with()


def test_passagem_repository_confirma_ciclo_em_uma_transacao():
    db = MagicMock()
    repository = PassagemRepository(db)
    ciclo = CicloPassagem(id=uuid.uuid4())

    resultado = repository.confirmar_ciclo(ciclo)

    assert resultado is ciclo
    db.commit.assert_called_once_with()
    db.refresh.assert_called_once_with(ciclo)
    db.rollback.assert_not_called()


def test_passagem_repository_desfaz_transacao_quando_commit_falha():
    db = MagicMock()
    db.commit.side_effect = SQLAlchemyError("falha simulada")
    repository = PassagemRepository(db)
    passagem = PassagemServico()

    with pytest.raises(PersistenciaError, match="concluir a operação"):
        repository.salvar(passagem)

    db.rollback.assert_called_once_with()
    db.refresh.assert_not_called()


def criar_passagem_completa_para_snapshot() -> PassagemServico:
    passagem_id = uuid.uuid4()
    linha = Linha(id=uuid.uuid4(), terminal=Terminal.BRISAMAR, codigo="22")
    radio = Radio(id=uuid.uuid4(), numero="R-01")
    return PassagemServico(
        id=passagem_id,
        terminal=Terminal.BRISAMAR,
        data=date(2026, 8, 14),
        turma=Turma.C,
        turno=Turno.DIURNO,
        responsavel_id=uuid.uuid4(),
        observacoes="Estado anterior",
        relatorio_ocorrencias="Sem ocorrências",
        mobile_utilizado=True,
        detalhe_brisamar=PassagemBrisamarDetalhe(
            id=uuid.uuid4(),
            passagem_id=passagem_id,
            radios_operantes=4,
            radios_inoperantes=1,
            baterias=5,
            carregadores=2,
        ),
        equipe=[
            EquipeMembro(
                id=uuid.uuid4(),
                passagem_id=passagem_id,
                nome="Manobrador",
                matricula="12345678",
            )
        ],
        ocupacoes_linhas=[
            PassagemLinhaOcupacao(
                id=uuid.uuid4(),
                passagem_id=passagem_id,
                linha_id=linha.id,
                linha=linha,
                veiculos="2 MK",
            )
        ],
        radios_utilizados=[
            PassagemRadioUso(
                id=uuid.uuid4(),
                passagem_id=passagem_id,
                radio_id=radio.id,
                radio=radio,
                manobrador_nome="Manobrador",
                hora_retirada=time(7, 0),
                apresentou_falha=False,
            )
        ],
    )


def test_passagem_repository_monta_snapshot_completo_e_serializavel():
    passagem = criar_passagem_completa_para_snapshot()

    snapshot = PassagemRepository.montar_snapshot(passagem)

    assert snapshot["passagem"]["id"] == str(passagem.id)
    assert snapshot["passagem"]["turma"] == "C"
    assert snapshot["passagem"]["turno"] == "DIURNO"
    assert snapshot["detalhe"]["radios_operantes"] == 4
    assert snapshot["equipe"][0]["matricula"] == "12345678"
    assert snapshot["ocupacoes_linhas"][0]["codigo_linha"] == "22"
    assert snapshot["radios_utilizados"][0]["numero_radio"] == "R-01"
    assert snapshot["radios_utilizados"][0]["hora_retirada"] == "07:00:00"
    json.dumps(snapshot)


def test_passagem_repository_registra_proxima_versao_sem_commit():
    db = MagicMock()
    db.query.return_value.filter.return_value.scalar.return_value = 2
    repository = PassagemRepository(db)
    passagem = criar_passagem_completa_para_snapshot()
    alterado_por = uuid.uuid4()

    historico = repository.registrar_snapshot(passagem, alterado_por)

    assert isinstance(historico, PassagemServicoHistorico)
    assert historico.versao == 3
    assert historico.alterado_por == alterado_por
    assert historico.snapshot["passagem"]["observacoes"] == "Estado anterior"
    db.add.assert_called_once_with(historico)
    db.flush.assert_called_once_with()
    db.commit.assert_not_called()


def test_passagem_repository_confirma_edicao_em_uma_transacao():
    db = MagicMock()
    repository = PassagemRepository(db)
    passagem = PassagemServico()

    resultado = repository.confirmar_edicao(passagem)

    assert resultado is passagem
    db.commit.assert_called_once_with()
    db.refresh.assert_called_once_with(passagem)
    db.rollback.assert_not_called()


def test_passagem_repository_desfaz_snapshot_e_edicao_quando_commit_falha():
    db = MagicMock()
    db.commit.side_effect = SQLAlchemyError("falha simulada")
    repository = PassagemRepository(db)

    with pytest.raises(PersistenciaError, match="concluir a operação"):
        repository.confirmar_edicao(PassagemServico())

    db.rollback.assert_called_once_with()
    db.refresh.assert_not_called()


def test_passagem_repository_consulta_detalhada_sem_bloquear_registro():
    db = MagicMock()
    consulta = db.query.return_value.options.return_value.filter.return_value
    passagem = criar_passagem_completa_para_snapshot()
    consulta.first.return_value = passagem
    repository = PassagemRepository(db)

    resultado = repository.buscar_por_id(passagem.id)

    assert resultado is passagem
    consulta.with_for_update.assert_not_called()
