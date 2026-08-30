import uuid
from datetime import date
from unittest.mock import MagicMock

import pytest

from app.features.auth.models import Usuario
from app.features.passagens.exceptions import PassagemError
from app.features.passagens.models import (
    CicloPassagem,
    EstadoCicloPassagem,
    PassagemServico,
    Terminal,
    Turma,
    Turno,
)
from app.features.passagens.schemas import CicloConsultaFiltros
from app.features.passagens.service import PassagemCicloService


def criar_ciclo(*terminais: Terminal) -> CicloPassagem:
    ciclo = CicloPassagem(
        id=uuid.uuid4(),
        data=date(2026, 8, 30),
        turma=Turma.C,
        turno=Turno.DIURNO,
        estado=EstadoCicloPassagem.RASCUNHO,
        criado_por=uuid.uuid4(),
    )
    ciclo.passagens = [
        PassagemServico(id=uuid.uuid4(), terminal=terminal) for terminal in terminais
    ]
    return ciclo


def test_confirmar_ciclo_exige_brisamar_e_tecon():
    repository = MagicMock()
    ciclo = criar_ciclo(Terminal.BRISAMAR)
    repository.buscar_ciclo_para_confirmacao.return_value = ciclo
    service = PassagemCicloService(repository)

    with pytest.raises(PassagemError, match="Brisamar e TECON"):
        service.confirmar(ciclo.id, Usuario(id=ciclo.criado_por))

    repository.confirmar_ciclo.assert_not_called()
    repository.desfazer.assert_called_once_with()


def test_confirmar_ciclo_bloqueia_as_duas_passagens_atomicamente():
    repository = MagicMock()
    ciclo = criar_ciclo(Terminal.BRISAMAR, Terminal.TECON)
    repository.buscar_ciclo_para_confirmacao.return_value = ciclo
    repository.confirmar_ciclo.side_effect = lambda registro: registro
    service = PassagemCicloService(repository)

    resultado = service.confirmar(ciclo.id, Usuario(id=ciclo.criado_por))

    assert resultado is ciclo
    assert ciclo.estado == EstadoCicloPassagem.CONFIRMADO
    assert ciclo.confirmado_em is not None
    repository.confirmar_ciclo.assert_called_once_with(ciclo)


def test_confirmar_ciclo_repetido_e_idempotente():
    repository = MagicMock()
    ciclo = criar_ciclo(Terminal.BRISAMAR, Terminal.TECON)
    ciclo.estado = EstadoCicloPassagem.CONFIRMADO
    repository.buscar_ciclo_para_confirmacao.return_value = ciclo
    service = PassagemCicloService(repository)

    resultado = service.confirmar(ciclo.id, Usuario(id=ciclo.criado_por))

    assert resultado is ciclo
    repository.confirmar_ciclo.assert_not_called()
    repository.desfazer.assert_called_once_with()


def test_confirmar_ciclo_rejeita_usuario_que_nao_criou_rascunho():
    repository = MagicMock()
    ciclo = criar_ciclo(Terminal.BRISAMAR, Terminal.TECON)
    repository.buscar_ciclo_para_confirmacao.return_value = ciclo
    service = PassagemCicloService(repository)

    with pytest.raises(PassagemError, match="autor do rascunho"):
        service.confirmar(ciclo.id, Usuario(id=uuid.uuid4()))

    repository.confirmar_ciclo.assert_not_called()
    repository.desfazer.assert_called_once_with()


def test_passagem_confirmada_nao_e_editavel_mesmo_durante_turno():
    ciclo = criar_ciclo(Terminal.BRISAMAR, Terminal.TECON)
    ciclo.estado = EstadoCicloPassagem.CONFIRMADO
    passagem = ciclo.passagens[0]
    passagem.ciclo = ciclo
    passagem.responsavel_id = ciclo.criado_por
    passagem.data = ciclo.data
    passagem.turma = ciclo.turma
    passagem.turno = ciclo.turno

    assert PassagemCicloService.passagem_confirmada(passagem) is True


def test_listagem_aplica_periodo_padrao_de_trinta_dias():
    repository = MagicMock()
    repository.listar_ciclos_confirmados.return_value = ([], 0)
    service = PassagemCicloService(repository)

    itens, total, data_inicio, data_fim = service.listar(
        CicloConsultaFiltros(), hoje=date(2026, 8, 30)
    )

    assert itens == []
    assert total == 0
    assert data_inicio == date(2026, 8, 1)
    assert data_fim == date(2026, 8, 30)
    repository.listar_ciclos_confirmados.assert_called_once_with(
        data_inicio=date(2026, 8, 1),
        data_fim=date(2026, 8, 30),
        turma=None,
        turno=None,
        responsavel=None,
        protocolo=None,
        pagina=1,
        por_pagina=20,
    )


def test_listagem_rejeita_inicio_posterior_ao_fim_padrao():
    repository = MagicMock()
    service = PassagemCicloService(repository)

    with pytest.raises(PassagemError, match="data final"):
        service.listar(
            CicloConsultaFiltros(data_inicio=date(2026, 8, 31)),
            hoje=date(2026, 8, 30),
        )

    repository.listar_ciclos_confirmados.assert_not_called()
