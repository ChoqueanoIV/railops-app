import pytest
from pydantic import ValidationError

from app.models.passagem import LadoLinha
from app.schemas.passagem_schema import (
    PassagemBrisamarEdicaoRequest,
    PassagemBrisamarRequest,
)


def dados_passagem_validos() -> dict:
    return {
        "data": "2026-08-13",
        "turma": "A",
        "turno": "DIURNO",
        "observacoes": "Sem alterações",
        "relatorio_ocorrencias": "Sem ocorrências",
        "mobile_utilizado": True,
        "equipe": [{"nome": "Operador de Teste", "matricula": "12345678"}],
        "ocupacoes_linhas": [
            {
                "codigo_linha": "22",
                "veiculos": "2MK + 5BOB",
                "sup_inf": "SUP",
            }
        ],
        "detalhe": {
            "radios_operantes": 4,
            "radios_inoperantes": 1,
            "baterias": 5,
            "carregadores": 2,
            "eots_disponiveis": "EOT 101",
            "eots_avariados": "Nenhum",
        },
        "radios_utilizados": [
            {
                "numero": "R-01",
                "manobrador_nome": "Operador de Teste",
                "hora_retirada": "07:00",
                "hora_entrega": "15:00",
                "apresentou_falha": False,
            }
        ],
    }


def test_passagem_brisamar_aceita_dados_validos():
    passagem = PassagemBrisamarRequest(**dados_passagem_validos())

    assert passagem.ocupacoes_linhas[0].sup_inf == LadoLinha.SUP
    assert passagem.detalhe.radios_operantes == 4


@pytest.mark.parametrize(
    ("campo", "valor"),
    (("turma", "E"), ("turno", "A"), ("turno", "MADRUGADA")),
)
def test_passagem_brisamar_rejeita_turma_ou_turno_desconhecido(campo, valor):
    dados = dados_passagem_validos()
    dados[campo] = valor

    with pytest.raises(ValidationError):
        PassagemBrisamarRequest(**dados)


def test_passagem_brisamar_exige_justificativa_sem_mobile():
    dados = dados_passagem_validos()
    dados["mobile_utilizado"] = False

    with pytest.raises(ValidationError, match="justificativa é obrigatória"):
        PassagemBrisamarRequest(**dados)


def test_passagem_brisamar_rejeita_quantidade_negativa():
    dados = dados_passagem_validos()
    dados["detalhe"]["radios_inoperantes"] = -1

    with pytest.raises(ValidationError):
        PassagemBrisamarRequest(**dados)


def test_passagem_brisamar_rejeita_equipe_com_matricula_invalida():
    dados = dados_passagem_validos()
    dados["equipe"][0]["matricula"] = "1234567"

    with pytest.raises(ValidationError):
        PassagemBrisamarRequest(**dados)


def test_passagem_brisamar_exige_ao_menos_uma_ocupacao():
    dados = dados_passagem_validos()
    dados["ocupacoes_linhas"] = []

    with pytest.raises(ValidationError):
        PassagemBrisamarRequest(**dados)


def test_passagem_brisamar_exige_descricao_quando_radio_falha():
    dados = dados_passagem_validos()
    dados["radios_utilizados"][0]["apresentou_falha"] = True

    with pytest.raises(ValidationError, match="descrição da falha é obrigatória"):
        PassagemBrisamarRequest(**dados)


def test_passagem_brisamar_remove_espacos_dos_textos():
    dados = dados_passagem_validos()
    dados["turma"] = "  A  "
    dados["turno"] = "  DIURNO  "
    dados["equipe"][0]["nome"] = "  Operador de Teste  "

    passagem = PassagemBrisamarRequest(**dados)

    assert passagem.turma.value == "A"
    assert passagem.turno.value == "DIURNO"
    assert passagem.equipe[0].nome == "Operador de Teste"


def test_edicao_brisamar_rejeita_alteracao_dos_campos_de_identidade():
    dados = dados_passagem_validos()
    dados.pop("turma")
    dados.pop("turno")

    with pytest.raises(ValidationError, match="data"):
        PassagemBrisamarEdicaoRequest(**dados)
