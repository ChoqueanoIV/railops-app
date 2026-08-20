import enum
import uuid
from datetime import date, datetime, time

from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload

from app.features.passagens.models import (
    Linha,
    PassagemLinhaOcupacao,
    PassagemRadioUso,
    PassagemServico,
    PassagemServicoHistorico,
    Radio,
    Terminal,
)
from app.shared.persistence.transactions import Transacao, TransacaoSQLAlchemy


class LinhaRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar_por_terminal(self, terminal: Terminal) -> list[Linha]:
        return (
            self.db.query(Linha)
            .filter(Linha.terminal == terminal)
            .order_by(Linha.codigo)
            .all()
        )


class RadioRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_ou_criar(self, numero: str) -> Radio:
        radio = self.db.query(Radio).filter(Radio.numero == numero).first()
        if radio is not None:
            return radio

        radio = Radio(numero=numero)
        self.db.add(radio)
        self.db.flush()
        return radio


class PassagemRepository:
    def __init__(self, db: Session, transacao: Transacao | None = None):
        self.db = db
        self.transacao = transacao or TransacaoSQLAlchemy(db)

    def salvar(self, passagem: PassagemServico) -> PassagemServico:
        self.db.add(passagem)
        self.transacao.confirmar()
        self.transacao.atualizar(passagem)
        return passagem

    def buscar_para_edicao(self, passagem_id: uuid.UUID) -> PassagemServico | None:
        return (
            self.db.query(PassagemServico)
            .options(
                selectinload(PassagemServico.detalhe_brisamar),
                selectinload(PassagemServico.detalhe_tecon),
                selectinload(PassagemServico.equipe),
                selectinload(PassagemServico.ocupacoes_linhas).selectinload(
                    PassagemLinhaOcupacao.linha
                ),
                selectinload(PassagemServico.radios_utilizados).selectinload(
                    PassagemRadioUso.radio
                ),
            )
            .filter(PassagemServico.id == passagem_id)
            .with_for_update()
            .first()
        )

    def buscar_por_id(self, passagem_id: uuid.UUID) -> PassagemServico | None:
        return (
            self.db.query(PassagemServico)
            .options(
                selectinload(PassagemServico.detalhe_brisamar),
                selectinload(PassagemServico.detalhe_tecon),
                selectinload(PassagemServico.equipe),
                selectinload(PassagemServico.ocupacoes_linhas).selectinload(
                    PassagemLinhaOcupacao.linha
                ),
                selectinload(PassagemServico.radios_utilizados).selectinload(
                    PassagemRadioUso.radio
                ),
            )
            .filter(PassagemServico.id == passagem_id)
            .first()
        )

    def registrar_snapshot(
        self, passagem: PassagemServico, alterado_por: uuid.UUID
    ) -> PassagemServicoHistorico:
        ultima_versao = (
            self.db.query(func.max(PassagemServicoHistorico.versao))
            .filter(PassagemServicoHistorico.passagem_id == passagem.id)
            .scalar()
        )
        historico = PassagemServicoHistorico(
            passagem_id=passagem.id,
            versao=(ultima_versao or 0) + 1,
            snapshot=self.montar_snapshot(passagem),
            alterado_por=alterado_por,
        )
        self.db.add(historico)
        self.db.flush()
        return historico

    def confirmar_edicao(self, passagem: PassagemServico) -> PassagemServico:
        self.transacao.confirmar()
        self.transacao.atualizar(passagem)
        return passagem

    def desfazer(self) -> None:
        self.transacao.desfazer()

    @classmethod
    def montar_snapshot(cls, passagem: PassagemServico) -> dict:
        detalhe = passagem.detalhe_brisamar or passagem.detalhe_tecon
        return {
            "passagem": cls._colunas_json(passagem),
            "detalhe": cls._colunas_json(detalhe) if detalhe is not None else None,
            "equipe": [cls._colunas_json(membro) for membro in passagem.equipe],
            "ocupacoes_linhas": [
                {
                    **cls._colunas_json(ocupacao),
                    "codigo_linha": ocupacao.linha.codigo,
                }
                for ocupacao in passagem.ocupacoes_linhas
            ],
            "radios_utilizados": [
                {
                    **cls._colunas_json(uso),
                    "numero_radio": uso.radio.numero,
                }
                for uso in passagem.radios_utilizados
            ],
        }

    @classmethod
    def _colunas_json(cls, registro) -> dict:
        return {
            coluna.name: cls._valor_json(getattr(registro, coluna.name))
            for coluna in registro.__table__.columns
        }

    @staticmethod
    def _valor_json(valor):
        if isinstance(valor, enum.Enum):
            return valor.value
        if isinstance(valor, uuid.UUID):
            return str(valor)
        if isinstance(valor, (date, datetime, time)):
            return valor.isoformat()
        return valor
