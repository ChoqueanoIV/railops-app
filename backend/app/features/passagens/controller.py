import uuid

from fastapi import APIRouter, Depends

from app.api.errors import ApiError, resposta_erro
from app.features.auth.dependencies import obter_usuario_atual
from app.features.auth.models import Usuario
from app.features.passagens.dependencies import obter_passagem_service
from app.features.passagens.exceptions import PassagemError
from app.features.passagens.schemas import (
    PassagemAtualizadaResponse,
    PassagemBrisamarEdicaoRequest,
    PassagemBrisamarRequest,
    PassagemConsultaResponse,
    PassagemCriadaResponse,
    PassagemTeconEdicaoRequest,
    PassagemTeconRequest,
)
from app.features.passagens.service import PassagemService

router = APIRouter(prefix="/passagens", tags=["Passagens de serviço"])


def montar_resposta_consulta(passagem, editavel):
    detalhe = passagem.detalhe_brisamar or passagem.detalhe_tecon
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
            {"nome": membro.nome, "matricula": membro.matricula}
            for membro in passagem.equipe
        ],
        ocupacoes_linhas=[
            {
                "codigo_linha": ocupacao.linha.codigo,
                "veiculos": ocupacao.veiculos,
                "sup_inf": ocupacao.sup_inf,
            }
            for ocupacao in passagem.ocupacoes_linhas
        ],
        detalhe={
            coluna.name: getattr(detalhe, coluna.name)
            for coluna in detalhe.__table__.columns
            if coluna.name not in {"id", "passagem_id"}
        },
        radios_utilizados=[
            {
                "numero": uso.radio.numero,
                "manobrador_nome": uso.manobrador_nome,
                "hora_retirada": uso.hora_retirada,
                "hora_entrega": uso.hora_entrega,
                "apresentou_falha": uso.apresentou_falha,
                "falha_descricao": uso.falha_descricao,
            }
            for uso in passagem.radios_utilizados
        ],
        editavel=editavel,
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
):
    try:
        passagem = service.criar_brisamar(dados, usuario_atual)
    except PassagemError as erro:
        raise ApiError(
            status_code=400, code="PASSAGEM_INVALID", message=str(erro)
        ) from erro

    return PassagemCriadaResponse(
        id=passagem.id,
        mensagem="Passagem de serviço registrada com sucesso.",
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
):
    try:
        passagem = service.criar_tecon(dados, usuario_atual)
    except PassagemError as erro:
        raise ApiError(
            status_code=400, code="PASSAGEM_INVALID", message=str(erro)
        ) from erro

    return PassagemCriadaResponse(
        id=passagem.id,
        mensagem="Passagem de serviço registrada com sucesso.",
    )


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
):
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
):
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
