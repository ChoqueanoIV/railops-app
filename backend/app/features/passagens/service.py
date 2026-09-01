import uuid
from datetime import UTC, date, datetime, time, timedelta
from typing import Protocol
from zoneinfo import ZoneInfo

from app.features.auth.models import Usuario
from app.features.passagens.exceptions import PassagemError
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
    Terminal,
    Turma,
    Turno,
)
from app.features.passagens.repository import (
    LinhaRepository,
    PassagemRepository,
    RadioRepository,
)
from app.features.passagens.schemas import (
    CicloConsultaFiltros,
    PassagemBrisamarEdicaoRequest,
    PassagemBrisamarRequest,
    PassagemTeconEdicaoRequest,
    PassagemTeconRequest,
)

FUSO_OPERACAO = ZoneInfo("America/Sao_Paulo")
PassagemEdicaoRequest = PassagemBrisamarEdicaoRequest | PassagemTeconEdicaoRequest


class CicloPassagemRepository(Protocol):
    def buscar_ciclo_para_confirmacao(
        self, ciclo_id: uuid.UUID
    ) -> CicloPassagem | None: ...

    def confirmar_ciclo(self, ciclo: CicloPassagem) -> CicloPassagem: ...

    def buscar_ciclo_por_identidade(
        self, data: date, turma: Turma, turno: Turno
    ) -> CicloPassagem | None: ...

    def buscar_ciclo_por_id(self, ciclo_id: uuid.UUID) -> CicloPassagem | None: ...

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
    ) -> tuple[list[CicloPassagem], int]: ...

    def desfazer(self) -> None: ...


class PassagemCicloService:
    def __init__(self, repository: CicloPassagemRepository):
        self.repository = repository

    def confirmar(self, ciclo_id: uuid.UUID, responsavel: Usuario) -> CicloPassagem:
        try:
            ciclo = self.repository.buscar_ciclo_para_confirmacao(ciclo_id)
            if ciclo is None:
                raise PassagemError("Ciclo de passagem não encontrado.")
            if ciclo.estado == EstadoCicloPassagem.CONFIRMADO:
                self.repository.desfazer()
                return ciclo
            if ciclo.criado_por != responsavel.id:
                raise PassagemError("Somente o autor do rascunho pode confirmá-lo.")

            terminais = {passagem.terminal for passagem in ciclo.passagens}
            if terminais != {Terminal.BRISAMAR, Terminal.TECON}:
                raise PassagemError(
                    "Brisamar e TECON devem estar preenchidos antes da confirmação."
                )

            ciclo.estado = EstadoCicloPassagem.CONFIRMADO
            ciclo.confirmado_em = datetime.now(UTC)
            return self.repository.confirmar_ciclo(ciclo)
        except Exception:
            self.repository.desfazer()
            raise

    def listar(
        self,
        filtros: CicloConsultaFiltros,
        hoje: date | None = None,
    ) -> tuple[list[CicloPassagem], int, date, date]:
        data_fim = filtros.data_fim or hoje or datetime.now(FUSO_OPERACAO).date()
        data_inicio = filtros.data_inicio or (data_fim - timedelta(days=29))
        if data_fim < data_inicio:
            raise PassagemError("A data final não pode ser anterior à data inicial.")
        itens, total = self.repository.listar_ciclos_confirmados(
            data_inicio=data_inicio,
            data_fim=data_fim,
            turma=filtros.turma,
            turno=filtros.turno,
            responsavel=filtros.responsavel,
            protocolo=filtros.protocolo,
            pagina=filtros.pagina,
            por_pagina=filtros.por_pagina,
        )
        return itens, total, data_inicio, data_fim

    def listar_para_exportacao(
        self,
        filtros: CicloConsultaFiltros,
        hoje: date | None = None,
    ) -> tuple[list[CicloPassagem], date, date]:
        data_fim = filtros.data_fim or hoje or datetime.now(FUSO_OPERACAO).date()
        data_inicio = filtros.data_inicio or (data_fim - timedelta(days=29))
        if data_fim < data_inicio:
            raise PassagemError("A data final não pode ser anterior à data inicial.")
        if data_fim - data_inicio > timedelta(days=365):
            raise PassagemError(
                "O período máximo para exportação é de um ano. "
                "Divida a consulta em arquivos separados."
            )

        itens: list[CicloPassagem] = []
        pagina = 1
        por_pagina = 100
        while True:
            lote, total = self.repository.listar_ciclos_confirmados(
                data_inicio=data_inicio,
                data_fim=data_fim,
                turma=filtros.turma,
                turno=filtros.turno,
                responsavel=filtros.responsavel,
                protocolo=filtros.protocolo,
                pagina=pagina,
                por_pagina=por_pagina,
            )
            itens.extend(lote)
            if len(itens) >= total or not lote:
                break
            pagina += 1
        return itens, data_inicio, data_fim

    def obter_por_id(self, ciclo_id: uuid.UUID, responsavel: Usuario) -> CicloPassagem:
        ciclo = self.repository.buscar_ciclo_por_id(ciclo_id)
        return self._validar_consulta(ciclo, responsavel)

    def obter_confirmado_para_exportacao(self, ciclo_id: uuid.UUID) -> CicloPassagem:
        ciclo = self.repository.buscar_ciclo_por_id(ciclo_id)
        if ciclo is None or ciclo.estado != EstadoCicloPassagem.CONFIRMADO:
            raise PassagemError("Passagem confirmada não encontrada.")
        return ciclo

    def obter_por_identidade(
        self,
        data: date,
        turma: Turma,
        turno: Turno,
        responsavel: Usuario,
    ) -> CicloPassagem:
        ciclo = self.repository.buscar_ciclo_por_identidade(data, turma, turno)
        return self._validar_consulta(ciclo, responsavel)

    @staticmethod
    def _validar_consulta(
        ciclo: CicloPassagem | None, responsavel: Usuario
    ) -> CicloPassagem:
        if ciclo is None:
            raise PassagemError("Ciclo de passagem não encontrado.")
        if (
            ciclo.estado == EstadoCicloPassagem.RASCUNHO
            and ciclo.criado_por != responsavel.id
        ):
            raise PassagemError("Somente o autor pode consultar este rascunho.")
        return ciclo

    @staticmethod
    def passagem_confirmada(passagem: PassagemServico) -> bool:
        return (
            passagem.ciclo is not None
            and passagem.ciclo.estado == EstadoCicloPassagem.CONFIRMADO
        )


class PassagemService:
    def __init__(
        self,
        passagem_repository: PassagemRepository,
        linha_repository: LinhaRepository,
        radio_repository: RadioRepository,
    ):
        self.passagem_repository = passagem_repository
        self.linha_repository = linha_repository
        self.radio_repository = radio_repository

    def criar_brisamar(
        self, dados: PassagemBrisamarRequest, responsavel: Usuario
    ) -> PassagemServico:
        linhas = self.linha_repository.listar_por_terminal(Terminal.BRISAMAR)
        linhas_por_codigo = {linha.codigo: linha for linha in linhas}
        codigos_informados = [
            ocupacao.codigo_linha for ocupacao in dados.ocupacoes_linhas
        ]

        if len(codigos_informados) != len(set(codigos_informados)):
            raise PassagemError("Cada linha deve ser informada uma única vez.")

        if set(codigos_informados) != set(linhas_por_codigo):
            raise PassagemError(
                "A ocupação de todas as linhas do Brisamar é obrigatória."
            )

        for ocupacao in dados.ocupacoes_linhas:
            linha = linhas_por_codigo[ocupacao.codigo_linha]
            if linha.permite_sup_inf and ocupacao.sup_inf is None:
                raise PassagemError(
                    f"A linha {linha.codigo} exige indicação SUP ou INF."
                )
            if not linha.permite_sup_inf and ocupacao.sup_inf is not None:
                raise PassagemError(
                    f"A linha {linha.codigo} não permite indicação SUP ou INF."
                )

        ciclo = self._obter_ciclo_para_terminal(dados, responsavel, Terminal.BRISAMAR)
        passagem = PassagemServico(
            ciclo=ciclo,
            terminal=Terminal.BRISAMAR,
            data=dados.data,
            turma=dados.turma,
            turno=dados.turno,
            responsavel_id=responsavel.id,
            observacoes=dados.observacoes,
            relatorio_ocorrencias=dados.relatorio_ocorrencias,
            mobile_utilizado=dados.mobile_utilizado,
            mobile_justificativa=dados.mobile_justificativa,
            detalhe_brisamar=PassagemBrisamarDetalhe(**dados.detalhe.model_dump()),
            equipe=[EquipeMembro(**membro.model_dump()) for membro in dados.equipe],
            ocupacoes_linhas=[
                PassagemLinhaOcupacao(
                    linha=linhas_por_codigo[ocupacao.codigo_linha],
                    veiculos=ocupacao.veiculos,
                    sup_inf=ocupacao.sup_inf,
                )
                for ocupacao in dados.ocupacoes_linhas
            ],
        )

        passagem.radios_utilizados = [
            PassagemRadioUso(
                radio=self.radio_repository.buscar_ou_criar(radio.numero),
                manobrador_nome=radio.manobrador_nome,
                hora_retirada=radio.hora_retirada,
                hora_entrega=radio.hora_entrega,
                apresentou_falha=radio.apresentou_falha,
                falha_descricao=radio.falha_descricao,
            )
            for radio in dados.radios_utilizados
        ]

        return self.passagem_repository.salvar(passagem)

    def criar_tecon(
        self, dados: PassagemTeconRequest, responsavel: Usuario
    ) -> PassagemServico:
        linhas = self.linha_repository.listar_por_terminal(Terminal.TECON)
        linhas_por_codigo = {linha.codigo: linha for linha in linhas}
        codigos_informados = [
            ocupacao.codigo_linha for ocupacao in dados.ocupacoes_linhas
        ]

        if len(codigos_informados) != len(set(codigos_informados)):
            raise PassagemError("Cada linha deve ser informada uma única vez.")

        if set(codigos_informados) != set(linhas_por_codigo):
            raise PassagemError("A ocupação de todas as linhas do TECON é obrigatória.")

        if any(ocupacao.sup_inf is not None for ocupacao in dados.ocupacoes_linhas):
            raise PassagemError("As linhas do TECON não permitem indicação SUP ou INF.")

        ciclo = self._obter_ciclo_para_terminal(dados, responsavel, Terminal.TECON)
        passagem = PassagemServico(
            ciclo=ciclo,
            terminal=Terminal.TECON,
            data=dados.data,
            turma=dados.turma,
            turno=dados.turno,
            responsavel_id=responsavel.id,
            observacoes=dados.observacoes,
            relatorio_ocorrencias=dados.relatorio_ocorrencias,
            mobile_utilizado=dados.mobile_utilizado,
            mobile_justificativa=dados.mobile_justificativa,
            detalhe_tecon=PassagemTeconDetalhe(**dados.detalhe.model_dump()),
            equipe=[EquipeMembro(**membro.model_dump()) for membro in dados.equipe],
            ocupacoes_linhas=[
                PassagemLinhaOcupacao(
                    linha=linhas_por_codigo[ocupacao.codigo_linha],
                    veiculos=ocupacao.veiculos,
                )
                for ocupacao in dados.ocupacoes_linhas
            ],
        )

        passagem.radios_utilizados = [
            PassagemRadioUso(
                radio=self.radio_repository.buscar_ou_criar(radio.numero),
                manobrador_nome=radio.manobrador_nome,
                hora_retirada=radio.hora_retirada,
                hora_entrega=radio.hora_entrega,
                apresentou_falha=radio.apresentou_falha,
                falha_descricao=radio.falha_descricao,
            )
            for radio in dados.radios_utilizados
        ]

        return self.passagem_repository.salvar(passagem)

    def _obter_ciclo_para_terminal(
        self,
        dados: PassagemBrisamarRequest | PassagemTeconRequest,
        responsavel: Usuario,
        terminal: Terminal,
    ) -> CicloPassagem:
        ciclo = self.passagem_repository.obter_ou_criar_ciclo(
            dados.data, dados.turma, dados.turno, responsavel.id
        )
        if ciclo.estado == EstadoCicloPassagem.CONFIRMADO:
            raise PassagemError("Este ciclo de passagem já foi confirmado.")
        if ciclo.criado_por != responsavel.id:
            raise PassagemError("Este ciclo pertence a outro responsável.")
        if any(passagem.terminal == terminal for passagem in ciclo.passagens):
            raise PassagemError(f"O terminal {terminal.value} já foi preenchido.")
        return ciclo

    def obter_para_edicao(
        self,
        passagem_id: uuid.UUID,
        responsavel: Usuario,
        agora: datetime | None = None,
    ) -> PassagemServico:
        passagem = self.passagem_repository.buscar_para_edicao(passagem_id)
        try:
            self.validar_permissao_edicao(passagem, responsavel, agora)
            assert passagem is not None
            return passagem
        except PassagemError:
            self.passagem_repository.desfazer()
            raise

    def obter_por_id(self, passagem_id: uuid.UUID) -> PassagemServico:
        passagem = self.passagem_repository.buscar_por_id(passagem_id)
        if passagem is None:
            raise PassagemError("Passagem de serviço não encontrada.")
        return passagem

    def consultar_historico(
        self, passagem_id: uuid.UUID, pagina: int, por_pagina: int
    ) -> tuple[PassagemServico, list[PassagemServicoHistorico], int]:
        passagem = self.obter_por_id(passagem_id)
        itens, total = self.passagem_repository.listar_historico(
            passagem_id, pagina, por_pagina
        )
        return passagem, itens, total

    @classmethod
    def passagem_editavel(
        cls,
        passagem: PassagemServico,
        responsavel: Usuario,
        agora: datetime | None = None,
    ) -> bool:
        try:
            cls.validar_permissao_edicao(passagem, responsavel, agora)
            return True
        except PassagemError:
            return False

    def editar_brisamar(
        self,
        passagem_id: uuid.UUID,
        dados: PassagemBrisamarEdicaoRequest,
        responsavel: Usuario,
        agora: datetime | None = None,
    ) -> PassagemServico:
        return self._editar(passagem_id, dados, responsavel, Terminal.BRISAMAR, agora)

    def editar_tecon(
        self,
        passagem_id: uuid.UUID,
        dados: PassagemTeconEdicaoRequest,
        responsavel: Usuario,
        agora: datetime | None = None,
    ) -> PassagemServico:
        return self._editar(passagem_id, dados, responsavel, Terminal.TECON, agora)

    def _editar(
        self,
        passagem_id: uuid.UUID,
        dados: PassagemEdicaoRequest,
        responsavel: Usuario,
        terminal: Terminal,
        agora: datetime | None,
    ) -> PassagemServico:
        try:
            passagem = self.passagem_repository.buscar_para_edicao(passagem_id)
            self.validar_permissao_edicao(passagem, responsavel, agora)
            assert passagem is not None
            if passagem.terminal != terminal:
                raise PassagemError(
                    f"Os dados informados não correspondem ao terminal {passagem.terminal.value}."
                )

            linhas_por_codigo = self._validar_linhas(dados, terminal)
            self.passagem_repository.registrar_snapshot(passagem, responsavel.id)
            self._aplicar_conteudo(passagem, dados, linhas_por_codigo, terminal)
            return self.passagem_repository.confirmar_edicao(passagem)
        except Exception:
            self.passagem_repository.desfazer()
            raise

    def _validar_linhas(
        self,
        dados: PassagemEdicaoRequest,
        terminal: Terminal,
    ) -> dict[str, Linha]:
        linhas = self.linha_repository.listar_por_terminal(terminal)
        linhas_por_codigo = {linha.codigo: linha for linha in linhas}
        codigos = [item.codigo_linha for item in dados.ocupacoes_linhas]
        if len(codigos) != len(set(codigos)):
            raise PassagemError("Cada linha deve ser informada uma única vez.")
        if set(codigos) != set(linhas_por_codigo):
            raise PassagemError(
                f"A ocupação de todas as linhas do {terminal.value.title()} é obrigatória."
            )
        for ocupacao in dados.ocupacoes_linhas:
            linha = linhas_por_codigo[ocupacao.codigo_linha]
            if linha.permite_sup_inf and ocupacao.sup_inf is None:
                raise PassagemError(
                    f"A linha {linha.codigo} exige indicação SUP ou INF."
                )
            if not linha.permite_sup_inf and ocupacao.sup_inf is not None:
                raise PassagemError(
                    f"A linha {linha.codigo} não permite indicação SUP ou INF."
                )
        return linhas_por_codigo

    def _aplicar_conteudo(
        self,
        passagem: PassagemServico,
        dados: PassagemEdicaoRequest,
        linhas_por_codigo: dict[str, Linha],
        terminal: Terminal,
    ) -> None:
        passagem.observacoes = dados.observacoes
        passagem.relatorio_ocorrencias = dados.relatorio_ocorrencias
        passagem.mobile_utilizado = dados.mobile_utilizado
        passagem.mobile_justificativa = dados.mobile_justificativa
        passagem.equipe = [EquipeMembro(**item.model_dump()) for item in dados.equipe]
        ocupacoes_por_codigo = {
            ocupacao.linha.codigo: ocupacao for ocupacao in passagem.ocupacoes_linhas
        }
        for item in dados.ocupacoes_linhas:
            ocupacao = ocupacoes_por_codigo[item.codigo_linha]
            ocupacao.veiculos = item.veiculos
            ocupacao.sup_inf = item.sup_inf
        passagem.radios_utilizados = [
            PassagemRadioUso(
                radio=self.radio_repository.buscar_ou_criar(item.numero),
                manobrador_nome=item.manobrador_nome,
                hora_retirada=item.hora_retirada,
                hora_entrega=item.hora_entrega,
                apresentou_falha=item.apresentou_falha,
                falha_descricao=item.falha_descricao,
            )
            for item in dados.radios_utilizados
        ]
        if terminal == Terminal.BRISAMAR:
            detalhe = passagem.detalhe_brisamar
        else:
            detalhe = passagem.detalhe_tecon
        for campo, valor in dados.detalhe.model_dump().items():
            setattr(detalhe, campo, valor)

    @classmethod
    def validar_permissao_edicao(
        cls,
        passagem: PassagemServico | None,
        responsavel: Usuario,
        agora: datetime | None = None,
    ) -> None:
        if passagem is None:
            raise PassagemError("Passagem de serviço não encontrada.")
        if PassagemCicloService.passagem_confirmada(passagem):
            raise PassagemError(
                "Esta passagem já foi confirmada e não pode ser editada."
            )
        if passagem.responsavel_id != responsavel.id:
            raise PassagemError("Somente o autor pode editar esta passagem.")
        if passagem.turma is None or passagem.turno is None:
            raise PassagemError(
                "Esta passagem é anterior à separação entre turma e turno e não pode ser editada."
            )

        momento = agora or datetime.now(FUSO_OPERACAO)
        if momento.tzinfo is None:
            momento = momento.replace(tzinfo=FUSO_OPERACAO)
        else:
            momento = momento.astimezone(FUSO_OPERACAO)

        inicio, encerramento = cls.calcular_janela_turno(passagem)
        if not inicio <= momento < encerramento:
            raise PassagemError(
                "A passagem só pode ser editada enquanto o próprio turno estiver em andamento."
            )

    @staticmethod
    def calcular_janela_turno(
        passagem: PassagemServico,
    ) -> tuple[datetime, datetime]:
        if passagem.turno == Turno.DIURNO:
            inicio = datetime.combine(passagem.data, time(7, 0), tzinfo=FUSO_OPERACAO)
            encerramento = datetime.combine(
                passagem.data, time(19, 0), tzinfo=FUSO_OPERACAO
            )
            return inicio, encerramento

        inicio = datetime.combine(passagem.data, time(19, 0), tzinfo=FUSO_OPERACAO)
        encerramento = datetime.combine(
            passagem.data + timedelta(days=1),
            time(7, 0),
            tzinfo=FUSO_OPERACAO,
        )
        return inicio, encerramento
