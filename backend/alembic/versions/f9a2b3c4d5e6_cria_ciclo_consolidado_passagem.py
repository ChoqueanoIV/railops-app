"""cria ciclo consolidado da passagem

Revision ID: f9a2b3c4d5e6
Revises: e8f1a2b3c4d5
Create Date: 2026-08-30 00:15:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "f9a2b3c4d5e6"
down_revision: str | Sequence[str] | None = "e8f1a2b3c4d5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    estado = postgresql.ENUM(
        "RASCUNHO",
        "CONFIRMADO",
        name="estadociclopassagem",
    )
    estado.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "ciclo_passagem",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("data", sa.Date(), nullable=False),
        sa.Column("turma", postgresql.ENUM(name="turma", create_type=False), nullable=False),
        sa.Column("turno", postgresql.ENUM(name="turno", create_type=False), nullable=False),
        sa.Column(
            "estado",
            postgresql.ENUM(name="estadociclopassagem", create_type=False),
            nullable=False,
            server_default="RASCUNHO",
        ),
        sa.Column("criado_por", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("confirmado_em", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["criado_por"], ["usuario.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "data", "turma", "turno", name="uq_ciclo_passagem_identidade"
        ),
    )
    op.add_column(
        "passagem_servico",
        sa.Column("ciclo_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_passagem_servico_ciclo_id",
        "passagem_servico",
        "ciclo_passagem",
        ["ciclo_id"],
        ["id"],
    )
    op.create_unique_constraint(
        "uq_passagem_servico_ciclo_terminal",
        "passagem_servico",
        ["ciclo_id", "terminal"],
    )


def downgrade() -> None:
    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM ciclo_passagem) THEN
                RAISE EXCEPTION
                    'Downgrade inseguro: existem ciclos de passagem persistidos';
            END IF;
        END $$;
        """
    )
    op.drop_constraint(
        "uq_passagem_servico_ciclo_terminal",
        "passagem_servico",
        type_="unique",
    )
    op.drop_constraint(
        "fk_passagem_servico_ciclo_id",
        "passagem_servico",
        type_="foreignkey",
    )
    op.drop_column("passagem_servico", "ciclo_id")
    op.drop_table("ciclo_passagem")
    postgresql.ENUM(name="estadociclopassagem").drop(
        op.get_bind(), checkfirst=True
    )
