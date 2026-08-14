from app.models.passagem import (
    EquipeMembro,
    PassagemBrisamarDetalhe,
    PassagemLinhaOcupacao,
    PassagemRadioUso,
    PassagemServico,
    PassagemTeconDetalhe,
    Terminal,
)
from app.models.usuario import Usuario
from app.repositories.passagem_repository import (
    LinhaRepository,
    PassagemRepository,
    RadioRepository,
)
from app.schemas.passagem_schema import PassagemBrisamarRequest, PassagemTeconRequest


class PassagemError(Exception):
    pass


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
            equipe=[
                EquipeMembro(**membro.model_dump()) for membro in dados.equipe
            ],
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
            equipe=[
                EquipeMembro(**membro.model_dump()) for membro in dados.equipe
            ],
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
