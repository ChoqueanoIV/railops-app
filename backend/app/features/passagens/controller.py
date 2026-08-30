import uuid
from datetime import date
from math import ceil
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.errors import ApiError, resposta_erro
from app.features.auth.dependencies import obter_usuario_atual
from app.features.auth.models import Usuario
from app.features.passagens.dependencies import (
    obter_ciclo_service,
    obter_passagem_service,
)
from app.features.passagens.exceptions import PassagemError
from app.features.passagens.models import (
    CicloPassagem,
    PassagemServico,
    Terminal,
    Turma,
    Turno,
)
from app.features.passagens.schemas import (
    BrisamarDetalheRequest,
    CicloConsultaFiltros,
    CicloConsultaItemResponse,
    CicloConsultaListaResponse,
    CicloPassagemResponse,
    EquipeMembroRequest,
    LinhaOcupacaoRequest,
    PaginacaoResponse,
    PassagemAtualizadaResponse,
    PassagemBrisamarEdicaoRequest,
    PassagemBrisamarRequest,
    PassagemConsultaResponse,
    PassagemCriadaResponse,
    PassagemTeconEdicaoRequest,
    PassagemTeconRequest,
    RadioUsoRequest,
    ResponsavelResumoResponse,
    TeconDetalheRequest,
)
from app.features.passagens.service import PassagemCicloService, PassagemService

router = APIRouter(prefix="/passagens", tags=["Passagens de serviço"])


def montar_resposta_consulta(
    passagem: PassagemServico, editavel: bool
) -> PassagemConsultaResponse:
    detalhe: BrisamarDetalheRequest | TeconDetalheRequest
    if passagem.detalhe_brisamar is not None:
        detalhe = BrisamarDetalheRequest.model_validate(
            passagem.detalhe_brisamar,
            from_attributes=True,
        )
    elif passagem.detalhe_tecon is not None:
        detalhe = TeconDetalheRequest.model_validate(
            passagem.detalhe_tecon,
            from_attributes=True,
        )
    else:
        raise RuntimeError("Passagem sem detalhe de terminal.")

    return PassagemConsultaResponse(
        id=passagem.id,
        terminal=passagem.terminal,
        data=passagem.data,
        turma=passagem.turma,
        turno=passagem.turno,
        observacoes=passagem.observacoes,
        relatorio_ocorrencias=passagem.relatorio_ocorrencias,
        mobile_utilizado=passagem.mobile_utilizado,
        mobile_justificativa=passagem.mobile_justificativa,
        equipe=[
            EquipeMembroRequest(nome=membro.nome, matricula=membro.matricula)
            for membro in passagem.equipe
        ],
        ocupacoes_linhas=[
            LinhaOcupacaoRequest(
                codigo_linha=ocupacao.linha.codigo,
                veiculos=ocupacao.veiculos,
                sup_inf=ocupacao.sup_inf,
            )
            for ocupacao in passagem.ocupacoes_linhas
        ],
        detalhe=detalhe,
        radios_utilizados=[
            RadioUsoRequest(
                numero=uso.radio.numero,
                manobrador_nome=uso.manobrador_nome,
                hora_retirada=uso.hora_retirada,
                hora_entrega=uso.hora_entrega,
                apresentou_falha=uso.apresentou_falha,
                falha_descricao=uso.falha_descricao,
            )
            for uso in passagem.radios_utilizados
        ],
        editavel=editavel,
    )


def terminal_pendente(ciclo: CicloPassagem) -> Terminal | None:
    preenchidos = {passagem.terminal for passagem in ciclo.passagens}
    pendentes = {Terminal.BRISAMAR, Terminal.TECON} - preenchidos
    return next(iter(pendentes)) if len(pendentes) == 1 else None


def montar_resposta_ciclo(
    ciclo: CicloPassagem,
    passagem_service: PassagemService,
    usuario_atual: Usuario,
) -> CicloPassagemResponse:
    return CicloPassagemResponse(
        id=ciclo.id,
        data=ciclo.data,
        turma=ciclo.turma,
        turno=ciclo.turno,
        estado=ciclo.estado,
        confirmado_em=ciclo.confirmado_em,
        terminal_pendente=terminal_pendente(ciclo),
        passagens=[
            montar_resposta_consulta(
                passagem,
                passagem_service.passagem_editavel(passagem, usuario_atual),
            )
            for passagem in ciclo.passagens
        ],
    )


@router.post(
    "/brisamar",
    response_model=PassagemCriadaResponse,
    status_code=201,
    summary="Registrar passagem de serviço do Brisamar",
    responses={
        400: resposta_erro("Regra de negócio inválida"),
        401: resposta_erro("Não autenticado"),
    },
)
def criar_passagem_brisamar(
    dados: PassagemBrisamarRequest,
    service: PassagemService = Depends(obter_passagem_service),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
) -> PassagemCriadaResponse:
    try:
        passagem = service.criar_brisamar(dados, usuario_atual)
    except PassagemError as erro:
        raise ApiError(
            status_code=400, code="PASSAGEM_INVALID", message=str(erro)
        ) from erro

    assert passagem.ciclo is not None
    return PassagemCriadaResponse(
        id=passagem.id,
        mensagem="Passagem de serviço registrada com sucesso.",
        ciclo_id=passagem.ciclo_id or passagem.ciclo.id,
        terminal_pendente=terminal_pendente(passagem.ciclo),
    )


@router.post(
    "/tecon",
    response_model=PassagemCriadaResponse,
    status_code=201,
    summary="Registrar passagem de serviço do TECON",
    responses={
        400: resposta_erro("Regra de negócio inválida"),
        401: resposta_erro("Não autenticado"),
    },
)
def criar_passagem_tecon(
    dados: PassagemTeconRequest,
    service: PassagemService = Depends(obter_passagem_service),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
) -> PassagemCriadaResponse:
    try:
        passagem = service.criar_tecon(dados, usuario_atual)
    except PassagemError as erro:
        raise ApiError(
            status_code=400, code="PASSAGEM_INVALID", message=str(erro)
        ) from erro

    assert passagem.ciclo is not None
    return PassagemCriadaResponse(
        id=passagem.id,
        mensagem="Passagem de serviço registrada com sucesso.",
        ciclo_id=passagem.ciclo_id or passagem.ciclo.id,
        terminal_pendente=terminal_pendente(passagem.ciclo),
    )


@router.get(
    "/ciclos",
    response_model=CicloConsultaListaResponse,
    summary="Listar ciclos confirmados",
    responses={401: resposta_erro("Não autenticado")},
)
def listar_ciclos_confirmados(
    filtros: Annotated[CicloConsultaFiltros, Query()],
    ciclo_service: PassagemCicloService = Depends(obter_ciclo_service),
    passagem_service: PassagemService = Depends(obter_passagem_service),
    _usuario_atual: Usuario = Depends(obter_usuario_atual),
) -> CicloConsultaListaResponse:
    try:
        ciclos, total, _, _ = ciclo_service.listar(filtros)
    except PassagemError as erro:
        raise ApiError(
            status_code=422, code="PASSAGEM_FILTER_INVALID", message=str(erro)
        ) from erro
    return CicloConsultaListaResponse(
        itens=[
            CicloConsultaItemResponse(
                **montar_resposta_ciclo(
                    ciclo, passagem_service, _usuario_atual
                ).model_dump(),
                responsavel=ResponsavelResumoResponse(
                    nome=ciclo.criador.nome,
                    matricula=ciclo.criador.matricula,
                ),
            )
            for ciclo in ciclos
        ],
        paginacao=PaginacaoResponse(
            pagina=filtros.pagina,
            por_pagina=filtros.por_pagina,
            total_itens=total,
            total_paginas=ceil(total / filtros.por_pagina),
        ),
    )


@router.get(
    "/ciclos/rascunho",
    response_model=CicloPassagemResponse,
    summary="Recuperar ciclo pela identidade operacional",
)
def consultar_ciclo_por_identidade(
    data: date,
    turma: Turma,
    turno: Turno,
    ciclo_service: PassagemCicloService = Depends(obter_ciclo_service),
    passagem_service: PassagemService = Depends(obter_passagem_service),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
) -> CicloPassagemResponse:
    try:
        ciclo = ciclo_service.obter_por_identidade(data, turma, turno, usuario_atual)
    except PassagemError as erro:
        raise ApiError(
            status_code=404, code="CICLO_NOT_FOUND", message=str(erro)
        ) from erro
    return montar_resposta_ciclo(ciclo, passagem_service, usuario_atual)


@router.get(
    "/ciclos/{ciclo_id}",
    response_model=CicloPassagemResponse,
    summary="Consultar revisão consolidada do ciclo",
)
def consultar_ciclo(
    ciclo_id: uuid.UUID,
    ciclo_service: PassagemCicloService = Depends(obter_ciclo_service),
    passagem_service: PassagemService = Depends(obter_passagem_service),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
) -> CicloPassagemResponse:
    try:
        ciclo = ciclo_service.obter_por_id(ciclo_id, usuario_atual)
    except PassagemError as erro:
        raise ApiError(
            status_code=404, code="CICLO_NOT_FOUND", message=str(erro)
        ) from erro
    return montar_resposta_ciclo(ciclo, passagem_service, usuario_atual)


@router.post(
    "/ciclos/{ciclo_id}/confirmar",
    response_model=CicloPassagemResponse,
    summary="Confirmar definitivamente o ciclo",
)
def confirmar_ciclo(
    ciclo_id: uuid.UUID,
    ciclo_service: PassagemCicloService = Depends(obter_ciclo_service),
    passagem_service: PassagemService = Depends(obter_passagem_service),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
) -> CicloPassagemResponse:
    try:
        ciclo = ciclo_service.confirmar(ciclo_id, usuario_atual)
    except PassagemError as erro:
        raise ApiError(
            status_code=400, code="CICLO_CONFIRMATION_INVALID", message=str(erro)
        ) from erro
    return montar_resposta_ciclo(ciclo, passagem_service, usuario_atual)


@router.put(
    "/{passagem_id}",
    response_model=PassagemAtualizadaResponse,
    summary="Editar passagem de serviço",
    responses={
        400: resposta_erro("Regra de negócio inválida"),
        401: resposta_erro("Não autenticado"),
    },
)
def editar_passagem(
    passagem_id: uuid.UUID,
    dados: PassagemBrisamarEdicaoRequest | PassagemTeconEdicaoRequest,
    service: PassagemService = Depends(obter_passagem_service),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
) -> PassagemAtualizadaResponse:
    try:
        if isinstance(dados, PassagemBrisamarEdicaoRequest):
            passagem = service.editar_brisamar(passagem_id, dados, usuario_atual)
        else:
            passagem = service.editar_tecon(passagem_id, dados, usuario_atual)
    except PassagemError as erro:
        raise ApiError(
            status_code=400, code="PASSAGEM_UPDATE_INVALID", message=str(erro)
        ) from erro

    return PassagemAtualizadaResponse(
        id=passagem.id,
        mensagem="Passagem de serviço atualizada com sucesso.",
    )


@router.get(
    "/{passagem_id}",
    response_model=PassagemConsultaResponse,
    summary="Consultar passagem de serviço",
    responses={
        401: resposta_erro("Não autenticado"),
        404: resposta_erro("Passagem não encontrada"),
    },
)
def consultar_passagem(
    passagem_id: uuid.UUID,
    service: PassagemService = Depends(obter_passagem_service),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
) -> PassagemConsultaResponse:
    try:
        passagem = service.obter_por_id(passagem_id)
    except PassagemError as erro:
        raise ApiError(
            status_code=404, code="PASSAGEM_NOT_FOUND", message=str(erro)
        ) from erro

    return montar_resposta_consulta(
        passagem,
        service.passagem_editavel(passagem, usuario_atual),
    )
