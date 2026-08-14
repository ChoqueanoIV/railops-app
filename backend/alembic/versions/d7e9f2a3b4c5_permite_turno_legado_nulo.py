"""permite turno legado nulo

Revision ID: d7e9f2a3b4c5
Revises: c6d8e1f2a3b4
Create Date: 2026-08-14 17:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d7e9f2a3b4c5"
down_revision: Union[str, Sequence[str], None] = "c6d8e1f2a3b4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "passagem_servico",
        "turno_legado",
        existing_type=sa.String(),
        nullable=True,
    )


def downgrade() -> None:
    op.execute(
        "UPDATE passagem_servico "
        "SET turno_legado = COALESCE(turma::text, 'LEGADO-SEM-TURMA') "
        "WHERE turno_legado IS NULL"
    )
    op.alter_column(
        "passagem_servico",
        "turno_legado",
        existing_type=sa.String(),
        nullable=False,
    )
