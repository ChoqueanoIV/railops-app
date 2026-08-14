"""separa turma e turno e cria historico

Revision ID: c6d8e1f2a3b4
Revises: b941bba1882e
Create Date: 2026-08-14 17:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "c6d8e1f2a3b4"
down_revision: Union[str, Sequence[str], None] = "b941bba1882e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


turma_enum = postgresql.ENUM(
    "A", "B", "C", "D", name="turma", create_type=False
)
turno_enum = postgresql.ENUM(
    "DIURNO", "NOTURNO", name="turno", create_type=False
)


def upgrade() -> None:
    bind = op.get_bind()
    turma_enum.create(bind, checkfirst=True)
    turno_enum.create(bind, checkfirst=True)

    op.alter_column(
        "passagem_servico", "turno", new_column_name="turno_legado"
    )
    op.add_column(
        "passagem_servico",
        sa.Column("turma", turma_enum, nullable=True),
    )
    op.add_column(
        "passagem_servico",
        sa.Column("turno", turno_enum, nullable=True),
    )

    op.create_table(
        "passagem_servico_historico",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("passagem_id", sa.UUID(), nullable=False),
        sa.Column("versao", sa.Integer(), nullable=False),
        sa.Column("snapshot", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "alterado_por", sa.UUID(), nullable=False
        ),
        sa.Column(
            "alterado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["alterado_por"], ["usuario.id"]),
        sa.ForeignKeyConstraint(["passagem_id"], ["passagem_servico.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "passagem_id", "versao", name="uq_historico_passagem_versao"
        ),
    )


def downgrade() -> None:
    op.drop_table("passagem_servico_historico")
    op.drop_column("passagem_servico", "turno")
    op.drop_column("passagem_servico", "turma")
    op.alter_column(
        "passagem_servico", "turno_legado", new_column_name="turno"
    )

    bind = op.get_bind()
    turno_enum.drop(bind, checkfirst=True)
    turma_enum.drop(bind, checkfirst=True)
