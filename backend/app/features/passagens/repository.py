import enum
import uuid
from datetime import date, datetime, time

from sqlalchemy import func, text
from sqlalchemy.orm import Session, selectinload

from app.features.auth.models import Usuario
from app.features.passagens.models import (
    CicloPassagem,
    EquipeMembro,
    EstadoCicloPassagem,
    Linha,
    PassagemBrisamarDetalhe,
    PassagemLinhaOcupacao,
    PassagemRadioUso,
    PassagemServico,
    PassagemServicoHistorico,
    PassagemTeconDetalhe,
    Radio,
    Terminal,
    Turma,
    Turno,
)
from app.shared.persistence.transactions import Transacao, TransacaoSQLAlchemy

RegistroSnapshot = (
    PassagemServico
    | PassagemBrisamarDetalhe
    | PassagemTeconDetalhe
    | EquipeMembro
    | PassagemLinhaOcupacao
    | PassagemRadioUso
)


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

    def obter_ou_criar_ciclo(
        self,
        data: date,
        turma: Turma,
        turno: Turno,
        criado_por: uuid.UUID,
    ) -> CicloPassagem:
        identidade = f"{data.isoformat()}|{turma.value}|{turno.value}"
        self.db.execute(
            text("SELECT pg_advisory_xact_lock(hashtextextended(:identidade, 0))"),
            {"identidade": identidade},
        )
        ciclo = (
            self.db.query(CicloPassagem)
            .options(selectinload(CicloPassagem.passagens))
            .filter(
                CicloPassagem.data == data,
                CicloPassagem.turma == turma,
                CicloPassagem.turno == turno,
            )
            .with_for_update()
            .first()
        )
        if ciclo is not None:
            return ciclo

        ciclo = CicloPassagem(
            data=data,
            turma=turma,
            turno=turno,
            estado=EstadoCicloPassagem.RASCUNHO,
            criado_por=criado_por,
        )
        self.db.add(ciclo)
        self.db.flush()
        return ciclo

    def buscar_ciclo_por_identidade(
        self, data: date, turma: Turma, turno: Turno
    ) -> CicloPassagem | None:
        return (
            self.db.query(CicloPassagem)
            .options(selectinload(CicloPassagem.passagens))
            .filter(
                CicloPassagem.data == data,
                CicloPassagem.turma == turma,
                CicloPassagem.turno == turno,
            )
            .first()
        )

    def buscar_ciclo_por_id(self, ciclo_id: uuid.UUID) -> CicloPassagem | None:
        return (
            self.db.query(CicloPassagem)
            .options(
                selectinload(CicloPassagem.criador),
                selectinload(CicloPassagem.passagens).selectinload(
                    PassagemServico.detalhe_brisamar
                ),
                selectinload(CicloPassagem.passagens).selectinload(
                    PassagemServico.detalhe_tecon
                ),
                selectinload(CicloPassagem.passagens).selectinload(
                    PassagemServico.equipe
                ),
                selectinload(CicloPassagem.passagens)
                .selectinload(PassagemServico.ocupacoes_linhas)
                .selectinload(PassagemLinhaOcupacao.linha),
                selectinload(CicloPassagem.passagens)
                .selectinload(PassagemServico.radios_utilizados)
                .selectinload(PassagemRadioUso.radio),
            )
            .filter(CicloPassagem.id == ciclo_id)
            .first()
        )

    def listar_ciclos_confirmados(
        self,
        *,
        data_inicio: date,
        data_fim: date,
        turma: Turma | None,
        turno: Turno | None,
        responsavel: str | None,
        protocolo: uuid.UUID | None,
        pagina: int,
        por_pagina: int,
    ) -> tuple[list[CicloPassagem], int]:
        consulta = (
            self.db.query(CicloPassagem)
            .options(
                selectinload(CicloPassagem.criador),
                selectinload(CicloPassagem.passagens).selectinload(
                    PassagemServico.detalhe_brisamar
                ),
                selectinload(CicloPassagem.passagens).selectinload(
                    PassagemServico.detalhe_tecon
                ),
                selectinload(CicloPassagem.passagens).selectinload(
                    PassagemServico.equipe
                ),
                selectinload(CicloPassagem.passagens)
                .selectinload(PassagemServico.ocupacoes_linhas)
                .selectinload(PassagemLinhaOcupacao.linha),
                selectinload(CicloPassagem.passagens)
                .selectinload(PassagemServico.radios_utilizados)
                .selectinload(PassagemRadioUso.radio),
            )
            .filter(
                CicloPassagem.estado == EstadoCicloPassagem.CONFIRMADO,
                CicloPassagem.data >= data_inicio,
                CicloPassagem.data <= data_fim,
            )
        )
        if turma is not None:
            consulta = consulta.filter(CicloPassagem.turma == turma)
        if turno is not None:
            consulta = consulta.filter(CicloPassagem.turno == turno)
        if protocolo is not None:
            consulta = consulta.filter(CicloPassagem.id == protocolo)
        if responsavel is not None:
            consulta = consulta.join(CicloPassagem.criador)
            if len(responsavel) == 8 and responsavel.isdigit():
                consulta = consulta.filter(Usuario.matricula == responsavel)
            else:
                trecho = (
                    responsavel.replace("\\", "\\\\")
                    .replace("%", "\\%")
                    .replace("_", "\\_")
                )
                consulta = consulta.filter(
                    Usuario.nome.ilike(f"%{trecho}%", escape="\\")
                )

        total = consulta.order_by(None).count()
        itens = (
            consulta.order_by(
                CicloPassagem.confirmado_em.desc(),
                CicloPassagem.id.desc(),
            )
            .offset((pagina - 1) * por_pagina)
            .limit(por_pagina)
            .all()
        )
        return itens, total

    def buscar_ciclo_para_confirmacao(
        self, ciclo_id: uuid.UUID
    ) -> CicloPassagem | None:
        return (
            self.db.query(CicloPassagem)
            .options(selectinload(CicloPassagem.passagens))
            .filter(CicloPassagem.id == ciclo_id)
            .with_for_update()
            .first()
        )

    def confirmar_ciclo(self, ciclo: CicloPassagem) -> CicloPassagem:
        self.transacao.confirmar()
        self.transacao.atualizar(ciclo)
        return ciclo

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

    def listar_historico(
        self, passagem_id: uuid.UUID, pagina: int, por_pagina: int
    ) -> tuple[list[PassagemServicoHistorico], int]:
        consulta = self.db.query(PassagemServicoHistorico).filter(
            PassagemServicoHistorico.passagem_id == passagem_id
        )
        total = consulta.count()
        itens = (
            consulta.options(selectinload(PassagemServicoHistorico.alterador))
            .order_by(
                PassagemServicoHistorico.versao.desc(),
                PassagemServicoHistorico.alterado_em.desc(),
            )
            .offset((pagina - 1) * por_pagina)
            .limit(por_pagina)
            .all()
        )
        return itens, total

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
    def montar_snapshot(cls, passagem: PassagemServico) -> dict[str, object]:
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
    def _colunas_json(cls, registro: RegistroSnapshot) -> dict[str, object]:
        return {
            coluna.name: cls._valor_json(getattr(registro, coluna.name))
            for coluna in registro.__table__.columns
        }

    @staticmethod
    def _valor_json(valor: object) -> object:
        if isinstance(valor, enum.Enum):
            return valor.value
        if isinstance(valor, uuid.UUID):
            return str(valor)
        if isinstance(valor, (date, datetime, time)):
            return valor.isoformat()
        return valor
