from pydantic import BaseModel, Field


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
