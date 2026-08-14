from datetime import date, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.passagem import LadoLinha


class SchemaBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)


class EquipeMembroRequest(SchemaBase):
    nome: str = Field(min_length=1)
    matricula: str = Field(pattern=r"^\d{8}$")


class LinhaOcupacaoRequest(SchemaBase):
    codigo_linha: str = Field(min_length=1)
    veiculos: str | None = None
    sup_inf: LadoLinha | None = None


class BrisamarDetalheRequest(SchemaBase):
    radios_operantes: int = Field(ge=0)
    radios_inoperantes: int = Field(ge=0)
    baterias: int = Field(ge=0)
    carregadores: int = Field(ge=0)
    eots_disponiveis: str | None = None
    eots_avariados: str | None = None


class RadioUsoRequest(SchemaBase):
    numero: str = Field(min_length=1)
    manobrador_nome: str = Field(min_length=1)
    hora_retirada: time | None = None
    hora_entrega: time | None = None
    apresentou_falha: bool = False
    falha_descricao: str | None = None

    @model_validator(mode="after")
    def validar_descricao_falha(self):
        if self.apresentou_falha and not self.falha_descricao:
            raise ValueError(
                "A descrição da falha é obrigatória quando o rádio apresentou falha."
            )
        return self


class PassagemBrisamarRequest(SchemaBase):
    data: date
    turno: str = Field(min_length=1)
    observacoes: str | None = None
    relatorio_ocorrencias: str | None = None
    mobile_utilizado: bool
    mobile_justificativa: str | None = None
    equipe: list[EquipeMembroRequest] = Field(default_factory=list)
    ocupacoes_linhas: list[LinhaOcupacaoRequest] = Field(min_length=1)
    detalhe: BrisamarDetalheRequest
    radios_utilizados: list[RadioUsoRequest] = Field(default_factory=list)

    @model_validator(mode="after")
    def validar_justificativa_mobile(self):
        if not self.mobile_utilizado and not self.mobile_justificativa:
            raise ValueError(
                "A justificativa é obrigatória quando o Mobile não foi utilizado."
            )
        return self


class PassagemCriadaResponse(SchemaBase):
    id: UUID
    mensagem: str
