import csv
import uuid
from datetime import UTC, date, datetime
from io import StringIO

from app.features.auth.models import Usuario
from app.features.passagens.exports import (
    CsvPassagensConsolidadas,
    PdfPassagemIndividual,
    PdfPassagensConsolidadas,
)
from app.features.passagens.models import (
    CicloPassagem,
    EstadoCicloPassagem,
    PassagemServico,
    PassagemTeconDetalhe,
    Terminal,
    Turma,
    Turno,
)
from tests.integration.test_passagem_repository import (
    criar_passagem_completa_para_snapshot,
)


def criar_ciclo_confirmado_completo() -> CicloPassagem:
    responsavel = Usuario(
        id=uuid.uuid4(), nome="Responsável Operacional", matricula="30032552"
    )
    passagem = criar_passagem_completa_para_snapshot()
    tecon_id = uuid.uuid4()
    passagem_tecon = PassagemServico(
        id=tecon_id,
        terminal=Terminal.TECON,
        data=date(2026, 8, 31),
        turma=Turma.C,
        turno=Turno.DIURNO,
        responsavel_id=responsavel.id,
        observacoes="Operação TECON concluída",
        relatorio_ocorrencias="Sem ocorrências no TECON",
        mobile_utilizado=True,
        detalhe_tecon=PassagemTeconDetalhe(
            id=uuid.uuid4(),
            passagem_id=tecon_id,
            houve_atendimento=True,
            carga_mal_posicionada=False,
            area1_atendida=True,
            area1_inicio=datetime(2026, 8, 31, 8, 0).time(),
            area1_termino=datetime(2026, 8, 31, 9, 0).time(),
            area2_atendida=False,
        ),
        equipe=[],
        ocupacoes_linhas=[],
        radios_utilizados=[],
    )
    ciclo = CicloPassagem(
        id=uuid.uuid4(),
        data=date(2026, 8, 31),
        turma=Turma.C,
        turno=Turno.DIURNO,
        estado=EstadoCicloPassagem.CONFIRMADO,
        criado_por=responsavel.id,
        confirmado_em=datetime(2026, 8, 31, 18, 45, tzinfo=UTC),
        criador=responsavel,
        passagens=[passagem, passagem_tecon],
    )
    passagem.ciclo = ciclo
    passagem.terminal = Terminal.BRISAMAR
    return ciclo


def test_pdf_individual_possui_assinatura_e_paginas():
    conteudo = PdfPassagemIndividual().gerar(criar_ciclo_confirmado_completo())

    assert conteudo.startswith(b"%PDF-")
    assert b"/Type /Page" in conteudo
    assert len(conteudo) > 1_000


def test_pdf_individual_nao_serializa_campos_de_autenticacao():
    conteudo = PdfPassagemIndividual().gerar(criar_ciclo_confirmado_completo())

    for campo_proibido in (
        b"senha_hash",
        b"codigo_ativacao_hash",
        b"pin_definido",
        b"access_token",
    ):
        assert campo_proibido not in conteudo


def test_csv_consolidado_possui_uma_linha_por_ciclo_e_utf8():
    ciclo = criar_ciclo_confirmado_completo()

    conteudo = CsvPassagensConsolidadas().gerar([ciclo])
    linhas = list(csv.DictReader(StringIO(conteudo.decode("utf-8-sig"))))

    assert len(linhas) == 1
    assert linhas[0]["protocolo"] == str(ciclo.id)
    assert linhas[0]["responsavel_nome"] == "Responsável Operacional"
    assert "Manobrador (12345678)" in linhas[0]["equipe_brisamar"]
    assert linhas[0]["ocorrencias_tecon"] == "Sem ocorrências no TECON"


def test_csv_consolidado_protege_formula_de_planilha():
    ciclo = criar_ciclo_confirmado_completo()
    ciclo.criador.nome = '=HIPERLINK("https://exemplo.invalid")'

    conteudo = CsvPassagensConsolidadas().gerar([ciclo])
    linha = next(csv.DictReader(StringIO(conteudo.decode("utf-8-sig"))))

    assert linha["responsavel_nome"].startswith("'=")


def test_pdf_consolidado_possui_assinatura_e_nao_contem_credenciais():
    ciclo = criar_ciclo_confirmado_completo()

    conteudo = PdfPassagensConsolidadas().gerar(
        [ciclo],
        date(2026, 8, 1),
        date(2026, 8, 31),
        datetime(2026, 8, 31, 19, 0, tzinfo=UTC),
    )

    assert conteudo.startswith(b"%PDF-")
    assert len(conteudo) > 1_000
    assert b"senha_hash" not in conteudo
    assert b"access_token" not in conteudo
