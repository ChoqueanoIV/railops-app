import uuid

import pytest

from app.api.errors import ApiError
from app.features.auth.dependencies import (
    exigir_consulta_historico,
    exigir_manobrador,
    exigir_perfil_especial,
)
from app.features.auth.models import PerfilUsuario, Usuario


@pytest.mark.parametrize(
    "perfil",
    [PerfilUsuario.INSTRUTOR, PerfilUsuario.MONITOR_QUALIDADE],
)
def test_perfil_especial_pode_consultar_historico(perfil):
    usuario = Usuario(id=uuid.uuid4(), perfil=perfil)

    assert exigir_consulta_historico(usuario) is usuario


def test_manobrador_nao_pode_consultar_historico():
    usuario = Usuario(id=uuid.uuid4(), perfil=PerfilUsuario.MANOBRADOR)

    with pytest.raises(ApiError) as erro:
        exigir_consulta_historico(usuario)

    assert erro.value.status_code == 403
    assert erro.value.code == "HISTORY_ACCESS_DENIED"


@pytest.mark.parametrize(
    "perfil", [PerfilUsuario.INSTRUTOR, PerfilUsuario.MONITOR_QUALIDADE]
)
def test_perfis_especiais_podem_exportar_consolidado(perfil):
    usuario = Usuario(id=uuid.uuid4(), perfil=perfil)

    assert exigir_perfil_especial(usuario) is usuario


def test_manobrador_nao_pode_exportar_consolidado():
    usuario = Usuario(id=uuid.uuid4(), perfil=PerfilUsuario.MANOBRADOR)

    with pytest.raises(ApiError) as erro:
        exigir_perfil_especial(usuario)

    assert erro.value.status_code == 403
    assert erro.value.code == "SPECIAL_ACCESS_DENIED"


def test_usuario_novo_assume_perfil_manobrador():
    coluna = Usuario.__table__.c.perfil

    assert coluna.nullable is False
    assert coluna.server_default.arg == "MANOBRADOR"


def test_manobrador_pode_preencher_passagem():
    usuario = Usuario(id=uuid.uuid4(), perfil=PerfilUsuario.MANOBRADOR)
    assert exigir_manobrador(usuario) is usuario


@pytest.mark.parametrize(
    "perfil", [PerfilUsuario.INSTRUTOR, PerfilUsuario.MONITOR_QUALIDADE]
)
def test_perfil_de_consulta_nao_pode_preencher_passagem(perfil):
    usuario = Usuario(id=uuid.uuid4(), perfil=perfil)
    with pytest.raises(ApiError) as erro:
        exigir_manobrador(usuario)
    assert erro.value.status_code == 403
    assert erro.value.code == "PASSAGE_WRITE_DENIED"
