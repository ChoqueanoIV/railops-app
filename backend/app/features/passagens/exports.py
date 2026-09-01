from __future__ import annotations

import csv
import json
from datetime import date, datetime
from html import escape
from io import BytesIO, StringIO
from typing import Iterable

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, StyleSheet1, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from app.features.passagens.models import CicloPassagem, PassagemServico, Terminal


def _texto(valor: object) -> str:
    if valor is None or valor == "":
        return "Não informado"
    if isinstance(valor, bool):
        return "Sim" if valor else "Não"
    return escape(str(valor))


def _passagem_terminal(
    ciclo: CicloPassagem, terminal: Terminal
) -> PassagemServico | None:
    return next(
        (passagem for passagem in ciclo.passagens if passagem.terminal == terminal),
        None,
    )


def _lista_deterministica(valores: Iterable[str]) -> str:
    return " | ".join(sorted(valores, key=str.casefold))


def _detalhe_json(passagem: PassagemServico | None) -> str:
    if passagem is None:
        return ""
    detalhe = passagem.detalhe_brisamar or passagem.detalhe_tecon
    if detalhe is None:
        return ""
    dados = {
        coluna.name: getattr(detalhe, coluna.name)
        for coluna in detalhe.__table__.columns
        if coluna.name not in {"id", "passagem_id"}
    }
    return json.dumps(dados, ensure_ascii=False, sort_keys=True, default=str)


def _csv_seguro(valor: object) -> str:
    texto = "" if valor is None else str(valor)
    if texto.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + texto
    return texto


class CsvPassagensConsolidadas:
    COLUNAS = (
        "protocolo",
        "data_inicio",
        "turma",
        "turno",
        "confirmado_em",
        "responsavel_nome",
        "responsavel_matricula",
        "equipe_brisamar",
        "equipe_tecon",
        "ocorrencias_brisamar",
        "ocorrencias_tecon",
        "observacoes_brisamar",
        "observacoes_tecon",
        "linhas_brisamar",
        "linhas_tecon",
        "radios_brisamar",
        "radios_tecon",
        "dados_brisamar",
        "dados_tecon",
    )

    def gerar(self, ciclos: Iterable[CicloPassagem]) -> bytes:
        arquivo = StringIO(newline="")
        escritor = csv.DictWriter(arquivo, fieldnames=self.COLUNAS, lineterminator="\n")
        escritor.writeheader()
        for ciclo in ciclos:
            escritor.writerow(
                {
                    chave: _csv_seguro(valor)
                    for chave, valor in self._linha(ciclo).items()
                }
            )
        return arquivo.getvalue().encode("utf-8-sig")

    @staticmethod
    def _linha(ciclo: CicloPassagem) -> dict[str, object]:
        brisamar = _passagem_terminal(ciclo, Terminal.BRISAMAR)
        tecon = _passagem_terminal(ciclo, Terminal.TECON)

        def equipe(passagem: PassagemServico | None) -> str:
            return _lista_deterministica(
                f"{membro.nome} ({membro.matricula})"
                for membro in (passagem.equipe if passagem is not None else [])
            )

        def linhas(passagem: PassagemServico | None) -> str:
            return _lista_deterministica(
                f"{ocupacao.linha.codigo}"
                f"{f' {ocupacao.sup_inf.value}' if ocupacao.sup_inf else ''}: "
                f"{ocupacao.veiculos}"
                for ocupacao in (
                    passagem.ocupacoes_linhas if passagem is not None else []
                )
            )

        def radios(passagem: PassagemServico | None) -> str:
            return _lista_deterministica(
                f"{uso.radio.numero}: {uso.manobrador_nome}"
                for uso in (passagem.radios_utilizados if passagem is not None else [])
            )

        return {
            "protocolo": ciclo.id,
            "data_inicio": ciclo.data.isoformat(),
            "turma": ciclo.turma.value,
            "turno": ciclo.turno.value,
            "confirmado_em": ciclo.confirmado_em.isoformat()
            if ciclo.confirmado_em
            else "",
            "responsavel_nome": ciclo.criador.nome,
            "responsavel_matricula": ciclo.criador.matricula,
            "equipe_brisamar": equipe(brisamar),
            "equipe_tecon": equipe(tecon),
            "ocorrencias_brisamar": brisamar.relatorio_ocorrencias if brisamar else "",
            "ocorrencias_tecon": tecon.relatorio_ocorrencias if tecon else "",
            "observacoes_brisamar": brisamar.observacoes if brisamar else "",
            "observacoes_tecon": tecon.observacoes if tecon else "",
            "linhas_brisamar": linhas(brisamar),
            "linhas_tecon": linhas(tecon),
            "radios_brisamar": radios(brisamar),
            "radios_tecon": radios(tecon),
            "dados_brisamar": _detalhe_json(brisamar),
            "dados_tecon": _detalhe_json(tecon),
        }


class PdfPassagensConsolidadas:
    def gerar(
        self,
        ciclos: list[CicloPassagem],
        data_inicio: date,
        data_fim: date,
        gerado_em: datetime,
    ) -> bytes:
        buffer = BytesIO()
        documento = BaseDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=14 * mm,
            rightMargin=14 * mm,
            topMargin=20 * mm,
            bottomMargin=18 * mm,
            title="Relatório consolidado de passagens",
            author="RailOps",
        )
        frame = Frame(
            documento.leftMargin,
            documento.bottomMargin,
            documento.width,
            documento.height,
            id="conteudo",
        )
        documento.addPageTemplates(
            PageTemplate(
                id="padrao",
                frames=[frame],
                onPage=PdfPassagemIndividual._cabecalho_rodape,
            )
        )
        estilos = getSampleStyleSheet()
        elementos: list[object] = [
            Paragraph("Relatório consolidado", estilos["Title"]),
            Spacer(1, 4 * mm),
            PdfPassagemIndividual._tabela(
                [
                    (
                        "Período",
                        f"{data_inicio.strftime('%d/%m/%Y')} a "
                        f"{data_fim.strftime('%d/%m/%Y')}",
                    ),
                    ("Gerado em", gerado_em.strftime("%d/%m/%Y %H:%M")),
                    ("Total", len(ciclos)),
                ]
            ),
            Spacer(1, 6 * mm),
        ]
        for ciclo in ciclos:
            brisamar = _passagem_terminal(ciclo, Terminal.BRISAMAR)
            tecon = _passagem_terminal(ciclo, Terminal.TECON)
            resumo = PdfPassagemIndividual._tabela(
                [
                    ("Protocolo", ciclo.id),
                    ("Data", ciclo.data.strftime("%d/%m/%Y")),
                    ("Turma / turno", f"{ciclo.turma.value} / {ciclo.turno.value}"),
                    (
                        "Responsável",
                        f"{ciclo.criador.nome} ({ciclo.criador.matricula})",
                    ),
                    (
                        "Confirmação",
                        ciclo.confirmado_em.strftime("%d/%m/%Y %H:%M")
                        if ciclo.confirmado_em
                        else None,
                    ),
                    (
                        "Brisamar",
                        brisamar.relatorio_ocorrencias if brisamar else None,
                    ),
                    ("TECON", tecon.relatorio_ocorrencias if tecon else None),
                ]
            )
            elementos.extend([KeepTogether([resumo]), Spacer(1, 5 * mm)])
        documento.build(elementos)
        return buffer.getvalue()


class PdfPassagemIndividual:
    def gerar(self, ciclo: CicloPassagem) -> bytes:
        buffer = BytesIO()
        documento = BaseDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=20 * mm,
            bottomMargin=18 * mm,
            title=f"Passagem de serviço {ciclo.id}",
            author="RailOps",
        )
        frame = Frame(
            documento.leftMargin,
            documento.bottomMargin,
            documento.width,
            documento.height,
            id="conteudo",
        )
        documento.addPageTemplates(
            PageTemplate(id="padrao", frames=[frame], onPage=self._cabecalho_rodape)
        )
        documento.build(self._conteudo(ciclo))
        return buffer.getvalue()

    @staticmethod
    def _cabecalho_rodape(canvas: Canvas, documento: BaseDocTemplate) -> None:
        canvas.saveState()
        canvas.setFont("Helvetica-Bold", 9)
        canvas.setFillColor(colors.HexColor("#17495E"))
        canvas.drawString(18 * mm, A4[1] - 12 * mm, "RailOps - Passagem de serviço")
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#52606D"))
        canvas.drawRightString(
            A4[0] - 18 * mm,
            10 * mm,
            f"Página {documento.page}",
        )
        canvas.restoreState()

    def _conteudo(self, ciclo: CicloPassagem) -> list[object]:
        estilos = getSampleStyleSheet()
        estilos.add(
            ParagraphStyle(
                name="TituloRailOps",
                parent=estilos["Title"],
                alignment=TA_CENTER,
                textColor=colors.HexColor("#17495E"),
                spaceAfter=6 * mm,
            )
        )
        elementos: list[object] = [
            Paragraph("Passagem completa", estilos["TituloRailOps"]),
            self._tabela(
                [
                    ("Protocolo", ciclo.id),
                    ("Data do início", ciclo.data.strftime("%d/%m/%Y")),
                    ("Turma", ciclo.turma.value),
                    ("Turno", ciclo.turno.value),
                    ("Responsável", ciclo.criador.nome),
                    ("Matrícula", ciclo.criador.matricula),
                    (
                        "Confirmada em",
                        ciclo.confirmado_em.strftime("%d/%m/%Y %H:%M")
                        if ciclo.confirmado_em
                        else None,
                    ),
                ]
            ),
            Spacer(1, 6 * mm),
        ]
        for passagem in sorted(ciclo.passagens, key=lambda item: item.terminal.value):
            elementos.extend(self._terminal(passagem, estilos))
        return elementos

    def _terminal(
        self, passagem: PassagemServico, estilos: StyleSheet1
    ) -> list[object]:
        nome = "Pátio Brisamar" if passagem.terminal == Terminal.BRISAMAR else "TECON"
        elementos: list[object] = [
            KeepTogether(
                [
                    Paragraph(nome, estilos["Heading2"]),
                    self._tabela(
                        [
                            ("Observações", passagem.observacoes),
                            (
                                "Relatório de ocorrências",
                                passagem.relatorio_ocorrencias,
                            ),
                            ("Mobile utilizado", passagem.mobile_utilizado),
                            ("Justificativa do Mobile", passagem.mobile_justificativa),
                        ]
                    ),
                ]
            )
        ]
        elementos.extend(self._secao_lista("Equipe", self._equipe(passagem), estilos))
        elementos.extend(
            self._secao_lista("Ocupação das linhas", self._linhas(passagem), estilos)
        )
        elementos.extend(
            self._secao_lista("Rádios utilizados", self._radios(passagem), estilos)
        )
        detalhe = passagem.detalhe_brisamar or passagem.detalhe_tecon
        if detalhe is not None:
            campos = [
                (coluna.name.replace("_", " "), getattr(detalhe, coluna.name))
                for coluna in detalhe.__table__.columns
                if coluna.name not in {"id", "passagem_id"}
            ]
            elementos.extend(self._secao_lista("Dados do terminal", campos, estilos))
        elementos.append(Spacer(1, 7 * mm))
        return elementos

    def _secao_lista(
        self, titulo: str, linhas: list[tuple[str, object]], estilos: StyleSheet1
    ) -> list[object]:
        return [
            Spacer(1, 3 * mm),
            Paragraph(titulo, estilos["Heading3"]),
            self._tabela(linhas or [("-", "Nenhum registro")]),
        ]

    @staticmethod
    def _equipe(passagem: PassagemServico) -> list[tuple[str, object]]:
        return [
            (membro.nome, f"Matrícula {membro.matricula}") for membro in passagem.equipe
        ]

    @staticmethod
    def _linhas(passagem: PassagemServico) -> list[tuple[str, object]]:
        return [
            (
                f"Linha {ocupacao.linha.codigo}"
                + (f" {ocupacao.sup_inf.value}" if ocupacao.sup_inf else ""),
                ocupacao.veiculos,
            )
            for ocupacao in passagem.ocupacoes_linhas
        ]

    @staticmethod
    def _radios(passagem: PassagemServico) -> list[tuple[str, object]]:
        return [
            (
                f"Rádio {uso.radio.numero}",
                f"{uso.manobrador_nome}; retirada {_texto(uso.hora_retirada)}; "
                f"entrega {_texto(uso.hora_entrega)}; falha {_texto(uso.apresentou_falha)}"
                + (f"; {uso.falha_descricao}" if uso.falha_descricao else ""),
            )
            for uso in passagem.radios_utilizados
        ]

    @staticmethod
    def _tabela(linhas: Iterable[tuple[str, object]]) -> Table:
        corpo = getSampleStyleSheet()["BodyText"]
        dados = [
            [
                Paragraph(
                    f"<b>{escape(str(rotulo)).capitalize()}</b>",
                    corpo,
                ),
                Paragraph(_texto(valor), corpo),
            ]
            for rotulo, valor in linhas
        ]
        tabela = Table(dados, colWidths=[48 * mm, 116 * mm], repeatRows=0)
        tabela.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C9D3DC")),
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF2F5")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )
        return tabela
