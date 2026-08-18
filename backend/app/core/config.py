import os
from pathlib import Path

from dotenv import load_dotenv

PASTA_BACKEND = Path(__file__).resolve().parents[2]
ARQUIVO_ENV = PASTA_BACKEND / ".env"

# O caminho explícito evita depender do diretório em que o comando foi iniciado.
load_dotenv(ARQUIVO_ENV)


def obter_variavel_obrigatoria(nome: str) -> str:
    valor = os.getenv(nome)
    if valor is None or not valor.strip():
        raise RuntimeError(
            f"{nome} não encontrada. Verifique se {ARQUIVO_ENV} existe "
            f"e contém a variável {nome}."
        )
    return valor
