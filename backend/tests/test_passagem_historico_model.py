from sqlalchemy import DateTime, Integer
from sqlalchemy.dialects.postgresql import JSONB

from app.features.passagens.models import (
    PassagemServico,
    PassagemServicoHistorico,
    Turma,
    Turno,
)


def test_passagem_separa_turma_de_turno():
    tabela = PassagemServico.__table__.c

    assert tabela.turno_legado.nullable is True
    assert tabela.turma.nullable is True
    assert tabela.turno.nullable is True
    assert set(tabela.turma.type.enums) == {turma.value for turma in Turma}
    assert set(tabela.turno.type.enums) == {turno.value for turno in Turno}


def test_historico_armazena_snapshot_e_dados_da_alteracao():
    tabela = PassagemServicoHistorico.__table__.c

    assert isinstance(tabela.versao.type, Integer)
    assert tabela.versao.nullable is False
    assert isinstance(tabela.snapshot.type, JSONB)
    assert tabela.snapshot.nullable is False
    assert tabela.alterado_por.nullable is False
    assert isinstance(tabela.alterado_em.type, DateTime)


def test_historico_possui_versao_unica_por_passagem():
    restricoes = PassagemServicoHistorico.__table__.constraints

    assert any(
        restricao.name == "uq_historico_passagem_versao" for restricao in restricoes
    )
    assert PassagemServico.historico.property.uselist is True
