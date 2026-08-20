import enum
import uuid
from datetime import date, datetime, time
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.features.auth.models import Usuario


def _modelo_usuario() -> type["Usuario"]:
    from app.features.auth.models import Usuario

    return Usuario


class Terminal(str, enum.Enum):
    BRISAMAR = "BRISAMAR"
    TECON = "TECON"


class LadoLinha(str, enum.Enum):
    SUP = "SUP"
    INF = "INF"


class Turma(str, enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class Turno(str, enum.Enum):
    DIURNO = "DIURNO"
    NOTURNO = "NOTURNO"


class PassagemServico(Base):
    __tablename__ = "passagem_servico"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    terminal: Mapped[Terminal] = mapped_column(Enum(Terminal), nullable=False)
    data: Mapped[date] = mapped_column(Date, nullable=False)
    # Os três campos permitem preservar os registros criados antes da separação.
    turno_legado: Mapped[str | None] = mapped_column(String, nullable=True)
    turma: Mapped[Turma | None] = mapped_column(
        Enum(Turma, name="turma"), nullable=True
    )
    turno: Mapped[Turno | None] = mapped_column(
        Enum(Turno, name="turno"), nullable=True
    )
    responsavel_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("usuario.id"), nullable=False
    )
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    relatorio_ocorrencias: Mapped[str | None] = mapped_column(Text, nullable=True)
    mobile_utilizado: Mapped[bool] = mapped_column(Boolean, nullable=False)
    mobile_justificativa: Mapped[str | None] = mapped_column(Text, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    responsavel: Mapped["Usuario"] = relationship(
        _modelo_usuario,
        back_populates="passagens",
    )
    detalhe_brisamar: Mapped["PassagemBrisamarDetalhe | None"] = relationship(
        back_populates="passagem", cascade="all, delete-orphan", uselist=False
    )
    detalhe_tecon: Mapped["PassagemTeconDetalhe | None"] = relationship(
        back_populates="passagem", cascade="all, delete-orphan", uselist=False
    )
    ocupacoes_linhas: Mapped[list["PassagemLinhaOcupacao"]] = relationship(
        back_populates="passagem", cascade="all, delete-orphan"
    )
    equipe: Mapped[list["EquipeMembro"]] = relationship(
        back_populates="passagem", cascade="all, delete-orphan"
    )
    radios_utilizados: Mapped[list["PassagemRadioUso"]] = relationship(
        back_populates="passagem", cascade="all, delete-orphan"
    )
    historico: Mapped[list["PassagemServicoHistorico"]] = relationship(
        back_populates="passagem", cascade="all, delete-orphan"
    )


class PassagemServicoHistorico(Base):
    __tablename__ = "passagem_servico_historico"
    __table_args__ = (
        UniqueConstraint("passagem_id", "versao", name="uq_historico_passagem_versao"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    passagem_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("passagem_servico.id"), nullable=False
    )
    versao: Mapped[int] = mapped_column(Integer, nullable=False)
    snapshot: Mapped[dict] = mapped_column(JSONB, nullable=False)
    alterado_por: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("usuario.id"), nullable=False
    )
    alterado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    passagem: Mapped["PassagemServico"] = relationship(back_populates="historico")


class PassagemBrisamarDetalhe(Base):
    __tablename__ = "passagem_brisamar_detalhe"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    passagem_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("passagem_servico.id"),
        unique=True,
        nullable=False,
    )
    radios_operantes: Mapped[int] = mapped_column(Integer, nullable=False)
    radios_inoperantes: Mapped[int] = mapped_column(Integer, nullable=False)
    baterias: Mapped[int] = mapped_column(Integer, nullable=False)
    carregadores: Mapped[int] = mapped_column(Integer, nullable=False)
    eots_disponiveis: Mapped[str | None] = mapped_column(Text, nullable=True)
    eots_avariados: Mapped[str | None] = mapped_column(Text, nullable=True)

    passagem: Mapped[PassagemServico] = relationship(back_populates="detalhe_brisamar")


class PassagemTeconDetalhe(Base):
    __tablename__ = "passagem_tecon_detalhe"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    passagem_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("passagem_servico.id"),
        unique=True,
        nullable=False,
    )
    houve_atendimento: Mapped[bool] = mapped_column(Boolean, nullable=False)
    carga_mal_posicionada: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    carga_mal_posicionada_descricao: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
    area1_atendida: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    area1_inicio: Mapped[time | None] = mapped_column(Time, nullable=True)
    area1_termino: Mapped[time | None] = mapped_column(Time, nullable=True)
    area2_atendida: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    area2_inicio: Mapped[time | None] = mapped_column(Time, nullable=True)
    area2_termino: Mapped[time | None] = mapped_column(Time, nullable=True)

    passagem: Mapped[PassagemServico] = relationship(back_populates="detalhe_tecon")


class Linha(Base):
    __tablename__ = "linha"
    __table_args__ = (
        UniqueConstraint("terminal", "codigo", name="uq_linha_terminal_codigo"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    terminal: Mapped[Terminal] = mapped_column(Enum(Terminal), nullable=False)
    codigo: Mapped[str] = mapped_column(String, nullable=False)
    permite_sup_inf: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    ocupacoes: Mapped[list["PassagemLinhaOcupacao"]] = relationship(
        back_populates="linha"
    )


class PassagemLinhaOcupacao(Base):
    __tablename__ = "passagem_linha_ocupacao"
    __table_args__ = (
        UniqueConstraint(
            "passagem_id",
            "linha_id",
            name="uq_passagem_linha_ocupacao_passagem_linha",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    passagem_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("passagem_servico.id"), nullable=False
    )
    linha_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("linha.id"), nullable=False
    )
    veiculos: Mapped[str | None] = mapped_column(Text, nullable=True)
    sup_inf: Mapped[LadoLinha | None] = mapped_column(Enum(LadoLinha), nullable=True)

    passagem: Mapped[PassagemServico] = relationship(back_populates="ocupacoes_linhas")
    linha: Mapped[Linha] = relationship(back_populates="ocupacoes")


class EquipeMembro(Base):
    __tablename__ = "equipe_membro"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    passagem_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("passagem_servico.id"), nullable=False
    )
    nome: Mapped[str] = mapped_column(String, nullable=False)
    matricula: Mapped[str] = mapped_column(String, nullable=False)

    passagem: Mapped[PassagemServico] = relationship(back_populates="equipe")


class Radio(Base):
    __tablename__ = "radio"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    numero: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    usos: Mapped[list["PassagemRadioUso"]] = relationship(back_populates="radio")


class PassagemRadioUso(Base):
    __tablename__ = "passagem_radio_uso"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    passagem_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("passagem_servico.id"), nullable=False
    )
    radio_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("radio.id"), nullable=False
    )
    manobrador_nome: Mapped[str] = mapped_column(String, nullable=False)
    hora_retirada: Mapped[time | None] = mapped_column(Time, nullable=True)
    hora_entrega: Mapped[time | None] = mapped_column(Time, nullable=True)
    apresentou_falha: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    falha_descricao: Mapped[str | None] = mapped_column(Text, nullable=True)

    passagem: Mapped[PassagemServico] = relationship(back_populates="radios_utilizados")
    radio: Mapped[Radio] = relationship(back_populates="usos")
