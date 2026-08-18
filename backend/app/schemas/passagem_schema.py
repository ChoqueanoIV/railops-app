from datetime import date, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.passagem import LadoLinha, Turma, Turno


class SchemaBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    @field_validator("*", mode="before")
    @classmethod
    def remover_espacos_antes_da_tipagem(cls, valor):
        return valor.strip() if isinstance(valor, str) else valor


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
    turma: Turma
    turno: Turno
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


class PassagemBrisamarEdicaoRequest(SchemaBase):
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


class PassagemAtualizadaResponse(SchemaBase):
    id: UUID
    mensagem: str


class TeconDetalheRequest(SchemaBase):
    houve_atendimento: bool
    carga_mal_posicionada: bool | None = None
    carga_mal_posicionada_descricao: str | None = None
    area1_atendida: bool | None = None
    area1_inicio: time | None = None
    area1_termino: time | None = None
    area2_atendida: bool | None = None
    area2_inicio: time | None = None
    area2_termino: time | None = None

    @model_validator(mode="after")
    def validar_atendimento_tecon(self):
        campos_especificos = (
            self.carga_mal_posicionada,
            self.carga_mal_posicionada_descricao,
            self.area1_atendida,
            self.area1_inicio,
            self.area1_termino,
            self.area2_atendida,
            self.area2_inicio,
            self.area2_termino,
        )

        if not self.houve_atendimento:
            if any(valor is not None for valor in campos_especificos):
                raise ValueError(
                    "Os campos específicos devem ficar vazios quando não houve atendimento."
                )
            return self

        if self.carga_mal_posicionada is None:
            raise ValueError("Informe se havia carga mal posicionada.")
        if self.area1_atendida is None or self.area2_atendida is None:
            raise ValueError("Informe separadamente o atendimento das Áreas 1 e 2.")

        if self.carga_mal_posicionada and not self.carga_mal_posicionada_descricao:
            raise ValueError(
                "Descreva a carga mal posicionada quando ela for identificada."
            )
        if not self.carga_mal_posicionada and self.carga_mal_posicionada_descricao:
            raise ValueError(
                "A descrição da carga deve ficar vazia quando não houver carga mal posicionada."
            )

        self._validar_horarios_area(
            "Área 1", self.area1_atendida, self.area1_inicio, self.area1_termino
        )
        self._validar_horarios_area(
            "Área 2", self.area2_atendida, self.area2_inicio, self.area2_termino
        )
        return self

    @staticmethod
    def _validar_horarios_area(
        nome: str,
        atendida: bool,
        inicio: time | None,
        termino: time | None,
    ) -> None:
        if atendida and (inicio is None or termino is None):
            raise ValueError(f"{nome} exige horários de início e término.")
        if not atendida and (inicio is not None or termino is not None):
            raise ValueError(
                f"Os horários de {nome} devem ficar vazios quando ela não foi atendida."
            )


class PassagemTeconRequest(SchemaBase):
    data: date
    turma: Turma
    turno: Turno
    observacoes: str = Field(min_length=1)
    relatorio_ocorrencias: str = Field(min_length=1)
    mobile_utilizado: bool
    mobile_justificativa: str | None = None
    equipe: list[EquipeMembroRequest] = Field(default_factory=list)
    ocupacoes_linhas: list[LinhaOcupacaoRequest] = Field(min_length=1)
    detalhe: TeconDetalheRequest
    radios_utilizados: list[RadioUsoRequest] = Field(default_factory=list)

    @model_validator(mode="after")
    def validar_justificativa_mobile(self):
        if not self.mobile_utilizado and not self.mobile_justificativa:
            raise ValueError(
                "A justificativa é obrigatória quando o Mobile não foi utilizado."
            )
        return self


class PassagemTeconEdicaoRequest(SchemaBase):
    observacoes: str = Field(min_length=1)
    relatorio_ocorrencias: str = Field(min_length=1)
    mobile_utilizado: bool
    mobile_justificativa: str | None = None
    equipe: list[EquipeMembroRequest] = Field(default_factory=list)
    ocupacoes_linhas: list[LinhaOcupacaoRequest] = Field(min_length=1)
    detalhe: TeconDetalheRequest
    radios_utilizados: list[RadioUsoRequest] = Field(default_factory=list)

    @model_validator(mode="after")
    def validar_justificativa_mobile(self):
        if not self.mobile_utilizado and not self.mobile_justificativa:
            raise ValueError(
                "A justificativa é obrigatória quando o Mobile não foi utilizado."
            )
        return self
