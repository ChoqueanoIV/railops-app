from pydantic import BaseModel


class PrimeiroAcessoRequest(BaseModel):
    matricula: str
    pin: str


class LoginRequest(BaseModel):
    matricula: str
    pin: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
