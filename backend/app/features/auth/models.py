import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.features.passagens.models import CicloPassagem, PassagemServico


def _modelo_passagem_servico() -> type["PassagemServico"]:
    from app.features.passagens.models import PassagemServico

    return PassagemServico


def _modelo_ciclo_passagem() -> type["CicloPassagem"]:
    from app.features.passagens.models import CicloPassagem

    return CicloPassagem


class PerfilUsuario(str, enum.Enum):
    MANOBRADOR = "MANOBRADOR"
    INSTRUTOR = "INSTRUTOR"
    MONITOR_QUALIDADE = "MONITOR_QUALIDADE"


class Usuario(Base):
    __tablename__ = "usuario"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    matricula: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    nome: Mapped[str] = mapped_column(String, nullable=False)
    senha_hash: Mapped[str | None] = mapped_column(String, nullable=True)
    codigo_ativacao_hash: Mapped[str | None] = mapped_column(String, nullable=True)
    pin_definido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    perfil: Mapped["PerfilUsuario"] = mapped_column(
        Enum(PerfilUsuario, name="perfilusuario"),
        nullable=False,
        default=lambda: PerfilUsuario.MANOBRADOR,
        server_default=PerfilUsuario.MANOBRADOR.value,
    )

    passagens: Mapped[list["PassagemServico"]] = relationship(
        _modelo_passagem_servico,
        back_populates="responsavel",
    )
    ciclos: Mapped[list["CicloPassagem"]] = relationship(
        _modelo_ciclo_passagem,
        back_populates="criador",
    )
