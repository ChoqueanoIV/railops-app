from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.shared.persistence.transactions import PersistenciaError, TransacaoSQLAlchemy


def test_transacao_confirma_sem_criar_nova_sessao():
    db = MagicMock()
    transacao = TransacaoSQLAlchemy(db)

    transacao.confirmar()

    db.commit.assert_called_once_with()
    db.rollback.assert_not_called()


def test_transacao_desfaz_e_oculta_erro_sqlalchemy_no_commit():
    db = MagicMock()
    db.commit.side_effect = SQLAlchemyError("detalhe interno")
    transacao = TransacaoSQLAlchemy(db)

    with pytest.raises(PersistenciaError) as erro:
        transacao.confirmar()

    assert "detalhe interno" not in str(erro.value)
    db.rollback.assert_called_once_with()


def test_transacao_desfaz_e_oculta_erro_sqlalchemy_no_refresh():
    db = MagicMock()
    db.refresh.side_effect = SQLAlchemyError("detalhe interno")
    transacao = TransacaoSQLAlchemy(db)

    with pytest.raises(PersistenciaError) as erro:
        transacao.atualizar(object())

    assert "detalhe interno" not in str(erro.value)
    db.rollback.assert_called_once_with()
