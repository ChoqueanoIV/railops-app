from sqlalchemy import Boolean, Text, Time

from app.features.passagens.models import PassagemServico, PassagemTeconDetalhe


def test_detalhe_tecon_possui_relacao_um_para_um_com_passagem():
    coluna = PassagemTeconDetalhe.__table__.c.passagem_id

    assert coluna.nullable is False
    assert coluna.unique is True
    assert PassagemServico.detalhe_tecon.property.uselist is False


def test_detalhe_tecon_permite_campos_condicionais_nulos():
    tabela = PassagemTeconDetalhe.__table__.c

    assert tabela.houve_atendimento.nullable is False
    assert isinstance(tabela.houve_atendimento.type, Boolean)

    campos_condicionais = (
        tabela.carga_mal_posicionada,
        tabela.carga_mal_posicionada_descricao,
        tabela.area1_atendida,
        tabela.area1_inicio,
        tabela.area1_termino,
        tabela.area2_atendida,
        tabela.area2_inicio,
        tabela.area2_termino,
    )
    assert all(campo.nullable for campo in campos_condicionais)
    assert isinstance(tabela.carga_mal_posicionada_descricao.type, Text)
    assert isinstance(tabela.area1_inicio.type, Time)
    assert isinstance(tabela.area2_termino.type, Time)
