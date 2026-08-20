import pytest
from pydantic import ValidationError

from app.features.passagens.schemas import PassagemTeconRequest

LINHAS_TECON = [
    "Viaduto/DM1A",
    "L1",
    "L2",
    "Travessão",
    "DM4",
    "DM6",
    "DM1",
    "DM3",
    "Funil/DM2",
]


def dados_tecon_validos() -> dict:
    return {
        "data": "2026-08-14",
        "turma": "C",
        "turno": "NOTURNO",
        "observacoes": "Sem alterações.",
        "relatorio_ocorrencias": "Sem ocorrências.",
        "mobile_utilizado": True,
        "equipe": [],
        "ocupacoes_linhas": [
            {"codigo_linha": codigo, "veiculos": "Livre"} for codigo in LINHAS_TECON
        ],
        "detalhe": {"houve_atendimento": False},
        "radios_utilizados": [],
    }


def test_tecon_sem_atendimento_aceita_apenas_nucleo():
    passagem = PassagemTeconRequest(**dados_tecon_validos())

    assert passagem.detalhe.houve_atendimento is False
    assert passagem.detalhe.area1_atendida is None


def test_tecon_sem_atendimento_rejeita_campos_especificos():
    dados = dados_tecon_validos()
    dados["detalhe"]["area1_atendida"] = False

    with pytest.raises(ValidationError, match="devem ficar vazios"):
        PassagemTeconRequest(**dados)


def test_tecon_com_atendimento_exige_vistoria_e_duas_areas():
    dados = dados_tecon_validos()
    dados["detalhe"] = {"houve_atendimento": True}

    with pytest.raises(ValidationError, match="carga mal posicionada"):
        PassagemTeconRequest(**dados)


def test_tecon_exige_descricao_de_carga_mal_posicionada():
    dados = dados_tecon_validos()
    dados["detalhe"] = {
        "houve_atendimento": True,
        "carga_mal_posicionada": True,
        "area1_atendida": False,
        "area2_atendida": False,
    }

    with pytest.raises(ValidationError, match="Descreva a carga"):
        PassagemTeconRequest(**dados)


def test_tecon_aceita_atendimento_parcial_na_area_1():
    dados = dados_tecon_validos()
    dados["detalhe"] = {
        "houve_atendimento": True,
        "carga_mal_posicionada": False,
        "area1_atendida": True,
        "area1_inicio": "08:00",
        "area1_termino": "09:30",
        "area2_atendida": False,
    }

    passagem = PassagemTeconRequest(**dados)

    assert passagem.detalhe.area1_atendida is True
    assert passagem.detalhe.area2_atendida is False


def test_tecon_aceita_atendimento_completo():
    dados = dados_tecon_validos()
    dados["detalhe"] = {
        "houve_atendimento": True,
        "carga_mal_posicionada": True,
        "carga_mal_posicionada_descricao": "Vagão com carga deslocada.",
        "area1_atendida": True,
        "area1_inicio": "08:00",
        "area1_termino": "09:00",
        "area2_atendida": True,
        "area2_inicio": "10:00",
        "area2_termino": "11:00",
    }

    passagem = PassagemTeconRequest(**dados)

    assert passagem.detalhe.carga_mal_posicionada is True
    assert passagem.detalhe.area2_atendida is True


def test_tecon_area_atendida_exige_horarios():
    dados = dados_tecon_validos()
    dados["detalhe"] = {
        "houve_atendimento": True,
        "carga_mal_posicionada": False,
        "area1_atendida": True,
        "area2_atendida": False,
    }

    with pytest.raises(ValidationError, match="Área 1 exige horários"):
        PassagemTeconRequest(**dados)


def test_tecon_area_nao_atendida_rejeita_horarios():
    dados = dados_tecon_validos()
    dados["detalhe"] = {
        "houve_atendimento": True,
        "carga_mal_posicionada": False,
        "area1_atendida": False,
        "area1_inicio": "08:00",
        "area2_atendida": False,
    }

    with pytest.raises(ValidationError, match="devem ficar vazios"):
        PassagemTeconRequest(**dados)


def test_tecon_exige_observacoes_e_ocorrencias():
    dados = dados_tecon_validos()
    dados["observacoes"] = "  "

    with pytest.raises(ValidationError):
        PassagemTeconRequest(**dados)
