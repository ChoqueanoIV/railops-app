import uuid
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


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
