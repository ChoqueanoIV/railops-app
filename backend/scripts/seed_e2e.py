from __future__ import annotations

import uuid
from dataclasses import dataclass
from urllib.parse import urlparse

from app.core.config import AmbienteAplicacao, obter_configuracao
from app.core.database import SessionLocal
from app.features.auth.models import PerfilUsuario, Usuario
from app.features.auth.service import pwd_context


@dataclass(frozen=True, slots=True)
class FixtureUsuario:
    id: uuid.UUID
    matricula: str
    nome: str
    perfil: PerfilUsuario
    codigo_ativacao: str | None = None
    pin: str | None = None


USUARIOS = (
    FixtureUsuario(
        id=uuid.UUID("00000000-0000-4000-8000-000000009101"),
        matricula="91000001",
        nome="Primeiro Acesso E2E",
        perfil=PerfilUsuario.MANOBRADOR,
        codigo_ativacao="654321",
    ),
    FixtureUsuario(
        id=uuid.UUID("00000000-0000-4000-8000-000000009102"),
        matricula="91000002",
        nome="Manobrador E2E",
        perfil=PerfilUsuario.MANOBRADOR,
        pin="1234",
    ),
    FixtureUsuario(
        id=uuid.UUID("00000000-0000-4000-8000-000000009103"),
        matricula="91000003",
        nome="Instrutor E2E",
        perfil=PerfilUsuario.INSTRUTOR,
        pin="1234",
    ),
)


def validar_destino() -> None:
    configuracao = obter_configuracao()
    destino = urlparse(configuracao.database_url)
    if configuracao.ambiente is not AmbienteAplicacao.TESTE:
        raise RuntimeError("Seed E2E exige RAILOPS_ENV=test.")
    if destino.hostname != "db" or destino.path != "/railops_e2e":
        raise RuntimeError("Seed E2E recusou banco fora do ambiente isolado.")


def preparar() -> None:
    validar_destino()
    with SessionLocal() as sessao:
        for dados in USUARIOS:
            existente = sessao.get(Usuario, dados.id)
            if existente is not None:
                continue
            sessao.add(
                Usuario(
                    id=dados.id,
                    matricula=dados.matricula,
                    nome=dados.nome,
                    perfil=dados.perfil,
                    codigo_ativacao_hash=(
                        pwd_context.hash(dados.codigo_ativacao)
                        if dados.codigo_ativacao
                        else None
                    ),
                    senha_hash=pwd_context.hash(dados.pin) if dados.pin else None,
                    pin_definido=dados.pin is not None,
                )
            )
        sessao.commit()


if __name__ == "__main__":
    preparar()
    print("Fixtures E2E preparadas no banco isolado.")
