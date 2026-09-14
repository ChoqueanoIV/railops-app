"""Registra condição dos celulares e Mobiles na passagem."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b3c4d5e6f7a8"
down_revision: str | Sequence[str] | None = "a2b3c4d5e6f7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("passagem_brisamar_detalhe", sa.Column("celular_eot_condicao", sa.Text(), nullable=True))
    op.add_column("passagem_brisamar_detalhe", sa.Column("mobiles_sala_quantidade", sa.Integer(), nullable=True))
    op.add_column("passagem_brisamar_detalhe", sa.Column("mobiles_sala_condicao", sa.Text(), nullable=True))
    op.add_column("passagem_tecon_detalhe", sa.Column("celular_tecon_condicao", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("passagem_tecon_detalhe", "celular_tecon_condicao")
    op.drop_column("passagem_brisamar_detalhe", "mobiles_sala_condicao")
    op.drop_column("passagem_brisamar_detalhe", "mobiles_sala_quantidade")
    op.drop_column("passagem_brisamar_detalhe", "celular_eot_condicao")
