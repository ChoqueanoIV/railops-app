from pydantic import BaseModel, Field

from app.features.auth.models import PerfilUsuario


class PrimeiroAcessoRequest(BaseModel):
    matricula: str = Field(pattern=r"^\d{8}$")
    codigo_ativacao: str = Field(pattern=r"^\d{6}$")
    pin: str = Field(pattern=r"^\d{4}$")


class LoginRequest(BaseModel):
    matricula: str = Field(pattern=r"^\d{8}$")
    pin: str = Field(pattern=r"^\d{4}$")


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UsuarioAtualResponse(BaseModel):
    nome: str
    matricula: str
    perfil: PerfilUsuario
