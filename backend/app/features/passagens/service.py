import uuid
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from app.features.auth.models import Usuario
from app.features.passagens.exceptions import PassagemError
from app.features.passagens.models import (
    EquipeMembro,
    PassagemBrisamarDetalhe,
    PassagemLinhaOcupacao,
    PassagemRadioUso,
    PassagemServico,
    PassagemTeconDetalhe,
    Terminal,
    Turno,
)
from app.features.passagens.repository import (
    LinhaRepository,
    PassagemRepository,
    RadioRepository,
)
from app.features.passagens.schemas import (
    PassagemBrisamarEdicaoRequest,
    PassagemBrisamarRequest,
    PassagemTeconEdicaoRequest,
    PassagemTeconRequest,
)

FUSO_OPERACAO = ZoneInfo("America/Sao_Paulo")


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

        passagem = PassagemServico(
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

        passagem = PassagemServico(
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

    def obter_para_edicao(
        self,
        passagem_id: uuid.UUID,
        responsavel: Usuario,
        agora: datetime | None = None,
    ) -> PassagemServico:
        passagem = self.passagem_repository.buscar_para_edicao(passagem_id)
        try:
            self.validar_permissao_edicao(passagem, responsavel, agora)
            return passagem
        except PassagemError:
            self.passagem_repository.desfazer()
            raise

    def obter_por_id(self, passagem_id: uuid.UUID) -> PassagemServico:
        passagem = self.passagem_repository.buscar_por_id(passagem_id)
        if passagem is None:
            raise PassagemError("Passagem de serviço não encontrada.")
        return passagem

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

    def _editar(self, passagem_id, dados, responsavel, terminal, agora):
        try:
            passagem = self.passagem_repository.buscar_para_edicao(passagem_id)
            self.validar_permissao_edicao(passagem, responsavel, agora)
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

    def _validar_linhas(self, dados, terminal):
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

    def _aplicar_conteudo(self, passagem, dados, linhas_por_codigo, terminal):
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
