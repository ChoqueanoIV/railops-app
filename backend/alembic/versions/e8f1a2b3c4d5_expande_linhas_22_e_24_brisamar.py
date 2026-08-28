"""expande linhas 22 e 24 do Brisamar

Revision ID: e8f1a2b3c4d5
Revises: d7e9f2a3b4c5
Create Date: 2026-08-28 16:20:00

"""

from collections.abc import Sequence

from alembic import op

revision: str = "e8f1a2b3c4d5"
down_revision: str | Sequence[str] | None = "d7e9f2a3b4c5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


LINHAS_NOVAS = (
    ("00000000-0000-4000-8000-000000002201", "22 SUP"),
    ("00000000-0000-4000-8000-000000002202", "22 INF"),
    ("00000000-0000-4000-8000-000000002299", "Travessão L22"),
    ("00000000-0000-4000-8000-000000002401", "24 SUP"),
    ("00000000-0000-4000-8000-000000002402", "24 INF"),
    ("00000000-0000-4000-8000-000000002499", "Travessão L24"),
)


def upgrade() -> None:
    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM passagem_linha_ocupacao AS ocupacao
                JOIN linha ON linha.id = ocupacao.linha_id
                WHERE linha.terminal = 'BRISAMAR'
                  AND linha.codigo IN ('22', '24')
                  AND ocupacao.sup_inf IS NULL
            ) THEN
                RAISE EXCEPTION
                    'Existem ocupações antigas de L22/L24 sem posição SUP/INF';
            END IF;
        END $$;
        """
    )
    valores = ",\n".join(
        f"('{linha_id}', 'BRISAMAR', '{codigo}', false)"
        for linha_id, codigo in LINHAS_NOVAS
    )
    op.execute(
        f"""
        INSERT INTO linha (id, terminal, codigo, permite_sup_inf) VALUES
        {valores}
        """
    )
    op.execute(
        """
        UPDATE passagem_linha_ocupacao AS ocupacao
        SET linha_id = nova.id,
            sup_inf = NULL
        FROM linha AS antiga, linha AS nova
        WHERE ocupacao.linha_id = antiga.id
          AND antiga.terminal = 'BRISAMAR'
          AND antiga.codigo IN ('22', '24')
          AND nova.terminal = 'BRISAMAR'
          AND nova.codigo = antiga.codigo || ' ' || ocupacao.sup_inf::text
        """
    )
    op.execute(
        """
        DELETE FROM linha
        WHERE terminal = 'BRISAMAR' AND codigo IN ('22', '24')
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM passagem_linha_ocupacao AS ocupacao
                JOIN linha ON linha.id = ocupacao.linha_id
                WHERE linha.terminal = 'BRISAMAR'
                  AND linha.codigo IN ('Travessão L22', 'Travessão L24')
                  AND ocupacao.veiculos IS NOT NULL
            ) THEN
                RAISE EXCEPTION
                    'Downgrade inseguro: existem travessões preenchidos';
            END IF;

            IF EXISTS (
                SELECT 1
                FROM passagem_linha_ocupacao AS sup
                JOIN linha AS linha_sup ON linha_sup.id = sup.linha_id
                JOIN passagem_linha_ocupacao AS inf
                  ON inf.passagem_id = sup.passagem_id
                JOIN linha AS linha_inf ON linha_inf.id = inf.linha_id
                WHERE linha_sup.codigo IN ('22 SUP', '24 SUP')
                  AND linha_inf.codigo = replace(linha_sup.codigo, ' SUP', ' INF')
                  AND sup.veiculos IS NOT NULL
                  AND inf.veiculos IS NOT NULL
            ) THEN
                RAISE EXCEPTION
                    'Downgrade inseguro: existem lados SUP e INF simultâneos';
            END IF;
        END $$;
        """
    )
    op.execute(
        """
        DELETE FROM passagem_linha_ocupacao AS ocupacao
        USING linha
        WHERE ocupacao.linha_id = linha.id
          AND linha.terminal = 'BRISAMAR'
          AND linha.codigo IN ('Travessão L22', 'Travessão L24')
        """
    )
    op.execute(
        """
        DELETE FROM passagem_linha_ocupacao AS sup
        USING linha AS linha_sup,
              passagem_linha_ocupacao AS inf,
              linha AS linha_inf
        WHERE sup.linha_id = linha_sup.id
          AND inf.passagem_id = sup.passagem_id
          AND inf.linha_id = linha_inf.id
          AND linha_sup.codigo IN ('22 SUP', '24 SUP')
          AND linha_inf.codigo = replace(linha_sup.codigo, ' SUP', ' INF')
          AND sup.veiculos IS NULL
          AND inf.veiculos IS NOT NULL
        """
    )
    op.execute(
        """
        DELETE FROM passagem_linha_ocupacao AS inf
        USING linha AS linha_inf,
              passagem_linha_ocupacao AS sup,
              linha AS linha_sup
        WHERE inf.linha_id = linha_inf.id
          AND sup.passagem_id = inf.passagem_id
          AND sup.linha_id = linha_sup.id
          AND linha_inf.codigo IN ('22 INF', '24 INF')
          AND linha_sup.codigo = replace(linha_inf.codigo, ' INF', ' SUP')
        """
    )
    op.execute(
        """
        INSERT INTO linha (id, terminal, codigo, permite_sup_inf) VALUES
        ('00000000-0000-4000-8000-000000000022', 'BRISAMAR', '22', true),
        ('00000000-0000-4000-8000-000000000024', 'BRISAMAR', '24', true)
        """
    )
    op.execute(
        """
        UPDATE passagem_linha_ocupacao AS ocupacao
        SET linha_id = antiga.id,
            sup_inf = CASE
                WHEN nova.codigo LIKE '% SUP' THEN 'SUP'::ladolinha
                ELSE 'INF'::ladolinha
            END
        FROM linha AS nova
        JOIN linha AS antiga
          ON antiga.terminal = 'BRISAMAR'
         AND antiga.codigo = replace(replace(nova.codigo, ' SUP', ''), ' INF', '')
        WHERE ocupacao.linha_id = nova.id
          AND nova.codigo IN ('22 SUP', '22 INF', '24 SUP', '24 INF')
        """
    )
    op.execute(
        """
        DELETE FROM linha
        WHERE terminal = 'BRISAMAR'
          AND codigo IN (
              '22 SUP', '22 INF', 'Travessão L22',
              '24 SUP', '24 INF', 'Travessão L24'
          )
        """
    )
