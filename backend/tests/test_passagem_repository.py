from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.models.passagem import Linha, PassagemServico, Radio, Terminal
from app.repositories.passagem_repository import (
    LinhaRepository,
    PassagemRepository,
    RadioRepository,
)


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


def test_passagem_repository_desfaz_transacao_quando_commit_falha():
    db = MagicMock()
    db.commit.side_effect = SQLAlchemyError("falha simulada")
    repository = PassagemRepository(db)
    passagem = PassagemServico()

    with pytest.raises(SQLAlchemyError, match="falha simulada"):
        repository.salvar(passagem)

    db.rollback.assert_called_once_with()
    db.refresh.assert_not_called()
