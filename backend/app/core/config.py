import os
from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

PASTA_BACKEND = Path(__file__).resolve().parents[2]
ARQUIVO_ENV = PASTA_BACKEND / ".env"

# O caminho explícito evita depender do diretório em que o comando foi iniciado.
# Variáveis já definidas pelo processo têm precedência sobre o arquivo local.
load_dotenv(ARQUIVO_ENV, override=False)


class AmbienteAplicacao(StrEnum):
    DESENVOLVIMENTO = "development"
    TESTE = "test"
    PRODUCAO = "production"


def obter_variavel_obrigatoria(
    nome: str,
    ambiente: Mapping[str, str] | None = None,
) -> str:
    origem = os.environ if ambiente is None else ambiente
    valor = origem.get(nome)
    if valor is None or not valor.strip():
        raise RuntimeError(
            f"{nome} não encontrada. Defina a variável no ambiente ou "
            f"verifique se {ARQUIVO_ENV} existe e contém {nome}."
        )
    return valor.strip()


@dataclass(frozen=True, slots=True)
class Configuracao:
    database_url: str
    jwt_secret_key: str
    ambiente: AmbienteAplicacao = AmbienteAplicacao.DESENVOLVIMENTO
    titulo_api: str = "RailOps API"
    cors_origins: tuple[str, ...] = (
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    )

    @classmethod
    def carregar(
        cls,
        ambiente: Mapping[str, str] | None = None,
    ) -> "Configuracao":
        origem = os.environ if ambiente is None else ambiente

        ambiente_bruto = origem.get("RAILOPS_ENV", "development").strip().lower()
        try:
            ambiente_aplicacao = AmbienteAplicacao(ambiente_bruto)
        except ValueError as erro:
            permitidos = ", ".join(item.value for item in AmbienteAplicacao)
            raise RuntimeError(
                f"RAILOPS_ENV inválido: {ambiente_bruto!r}. Use: {permitidos}."
            ) from erro

        origens_brutas = origem.get(
            "CORS_ORIGINS",
            "http://localhost:3000,http://127.0.0.1:3000",
        )
        cors_origins = tuple(
            origem_item.strip()
            for origem_item in origens_brutas.split(",")
            if origem_item.strip()
        )
        if not cors_origins:
            raise RuntimeError("CORS_ORIGINS deve conter ao menos uma origem válida.")

        jwt_secret_key = obter_variavel_obrigatoria("JWT_SECRET_KEY", origem)
        if ambiente_aplicacao is AmbienteAplicacao.PRODUCAO:
            if len(jwt_secret_key.encode()) < 32:
                raise RuntimeError(
                    "JWT_SECRET_KEY deve possuir ao menos 32 bytes em production."
                )
            if "*" in cors_origins:
                raise RuntimeError("CORS_ORIGINS não permite '*' em production.")

        return cls(
            database_url=obter_variavel_obrigatoria("DATABASE_URL", origem),
            jwt_secret_key=jwt_secret_key,
            ambiente=ambiente_aplicacao,
            titulo_api=origem.get("API_TITLE", "RailOps API").strip() or "RailOps API",
            cors_origins=cors_origins,
        )


@lru_cache(maxsize=1)
def obter_configuracao() -> Configuracao:
    return Configuracao.carregar()
