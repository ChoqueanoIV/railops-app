import uuid
from datetime import datetime, timedelta, timezone

import pytest
from jose import jwt
from pydantic import ValidationError

from app.models.usuario import Usuario
from app.schemas.auth_schema import LoginRequest, PrimeiroAcessoRequest
from app.services.auth_service import (
    ALGORITHM,
    SECRET_KEY,
    AuthService,
    AutenticacaoError,
    pwd_context,
)


class UsuarioRepositoryFake:
    def __init__(self, usuario: Usuario | None):
        self.usuario = usuario

    def buscar_por_matricula(self, matricula: str) -> Usuario | None:
        if self.usuario is None or self.usuario.matricula != matricula:
            return None
        return self.usuario

    def buscar_por_id(self, usuario_id: uuid.UUID) -> Usuario | None:
        if self.usuario is None or self.usuario.id != usuario_id:
            return None
        return self.usuario

    def ativar_usuario(self, usuario: Usuario, novo_pin_hash: str) -> Usuario:
        usuario.senha_hash = novo_pin_hash
        usuario.pin_definido = True
        usuario.codigo_ativacao_hash = None
        return usuario


def criar_usuario_nao_ativado(codigo_ativacao: str = "123456") -> Usuario:
    return Usuario(
        id=uuid.uuid4(),
        matricula="30032552",
        nome="Usuário de Teste",
        senha_hash=None,
        pin_definido=False,
        codigo_ativacao_hash=pwd_context.hash(codigo_ativacao),
    )


def test_primeiro_acesso_ativa_usuario_e_invalida_codigo():
    usuario = criar_usuario_nao_ativado()
    service = AuthService(UsuarioRepositoryFake(usuario))

    resultado = service.primeiro_acesso("30032552", "123456", "4321")

    assert resultado.pin_definido is True
    assert pwd_context.verify("4321", resultado.senha_hash)
    assert resultado.codigo_ativacao_hash is None


def test_primeiro_acesso_rejeita_codigo_incorreto():
    usuario = criar_usuario_nao_ativado()
    service = AuthService(UsuarioRepositoryFake(usuario))

    with pytest.raises(AutenticacaoError, match="Dados de ativação inválidos"):
        service.primeiro_acesso("30032552", "654321", "4321")

    assert usuario.pin_definido is False
    assert usuario.senha_hash is None
    assert usuario.codigo_ativacao_hash is not None


def test_primeiro_acesso_rejeita_matricula_inexistente():
    service = AuthService(UsuarioRepositoryFake(None))

    with pytest.raises(AutenticacaoError, match="Dados de ativação inválidos"):
        service.primeiro_acesso("99999999", "123456", "4321")


def test_primeiro_acesso_rejeita_usuario_ja_ativado():
    usuario = criar_usuario_nao_ativado()
    usuario.pin_definido = True
    usuario.senha_hash = pwd_context.hash("4321")
    service = AuthService(UsuarioRepositoryFake(usuario))

    with pytest.raises(AutenticacaoError, match="Dados de ativação inválidos"):
        service.primeiro_acesso("30032552", "123456", "5678")


def test_primeiro_acesso_rejeita_reutilizacao_do_codigo():
    usuario = criar_usuario_nao_ativado()
    service = AuthService(UsuarioRepositoryFake(usuario))

    service.primeiro_acesso("30032552", "123456", "4321")

    with pytest.raises(AutenticacaoError, match="Dados de ativação inválidos"):
        service.primeiro_acesso("30032552", "123456", "5678")


def test_primeiro_acesso_rejeita_codigo_fora_do_formato():
    with pytest.raises(ValidationError):
        PrimeiroAcessoRequest(
            matricula="30032552", codigo_ativacao="12345", pin="4321"
        )


def test_primeiro_acesso_rejeita_pin_fora_do_formato():
    with pytest.raises(ValidationError):
        PrimeiroAcessoRequest(
            matricula="30032552", codigo_ativacao="123456", pin="321"
        )


def test_validar_token_retorna_usuario():
    usuario = criar_usuario_nao_ativado()
    service = AuthService(UsuarioRepositoryFake(usuario))
    token = service._gerar_token(usuario)

    resultado = service.validar_token(token)

    assert resultado is usuario


def test_validar_token_rejeita_token_adulterado():
    usuario = criar_usuario_nao_ativado()
    service = AuthService(UsuarioRepositoryFake(usuario))

    with pytest.raises(AutenticacaoError, match="Token inválido ou expirado"):
        service.validar_token("token.adulterado.invalido")


def test_validar_token_rejeita_token_expirado():
    usuario = criar_usuario_nao_ativado()
    service = AuthService(UsuarioRepositoryFake(usuario))
    token = jwt.encode(
        {
            "sub": str(usuario.id),
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    with pytest.raises(AutenticacaoError, match="Token inválido ou expirado"):
        service.validar_token(token)


def test_validar_token_rejeita_usuario_inexistente():
    usuario = criar_usuario_nao_ativado()
    token = AuthService(UsuarioRepositoryFake(usuario))._gerar_token(usuario)
    service = AuthService(UsuarioRepositoryFake(None))

    with pytest.raises(AutenticacaoError, match="Token inválido ou expirado"):
        service.validar_token(token)


def test_login_valido_retorna_jwt_com_identidade_atual():
    usuario = criar_usuario_nao_ativado()
    usuario.pin_definido = True
    usuario.senha_hash = pwd_context.hash("4321")
    service = AuthService(UsuarioRepositoryFake(usuario))

    token = service.login(usuario.matricula, "4321")
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert payload["sub"] == str(usuario.id)
    assert payload["matricula"] == usuario.matricula
    assert "exp" in payload


@pytest.mark.parametrize(
    ("usuario", "pin"),
    (
        (None, "4321"),
        (criar_usuario_nao_ativado(), "4321"),
    ),
)
def test_login_rejeita_matricula_inexistente_ou_usuario_nao_ativado(usuario, pin):
    service = AuthService(UsuarioRepositoryFake(usuario))

    with pytest.raises(AutenticacaoError, match="Matrícula ou PIN inválidos"):
        service.login("30032552", pin)


def test_login_rejeita_pin_incorreto_sem_diferenciar_credencial():
    usuario = criar_usuario_nao_ativado()
    usuario.pin_definido = True
    usuario.senha_hash = pwd_context.hash("4321")
    service = AuthService(UsuarioRepositoryFake(usuario))

    with pytest.raises(AutenticacaoError, match="Matrícula ou PIN inválidos"):
        service.login(usuario.matricula, "9999")


def test_login_exige_matricula_com_oito_digitos_e_pin_com_quatro():
    with pytest.raises(ValidationError):
        LoginRequest(matricula="1234567", pin="12345")
