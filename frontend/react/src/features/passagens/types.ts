export type Terminal = 'BRISAMAR' | 'TECON';
export type Turma = 'A' | 'B' | 'C' | 'D';
export type Turno = 'DIURNO' | 'NOTURNO';

export interface EquipeMembro {
  nome: string;
  matricula: string;
}
export interface LinhaOcupacao {
  codigo_linha: string;
  veiculos: string | null;
  sup_inf: 'SUP' | 'INF' | null;
}
export interface RadioUso {
  numero: string;
  manobrador_nome: string;
  hora_retirada: string | null;
  hora_entrega: string | null;
  apresentou_falha: boolean;
  falha_descricao: string | null;
}
export interface BrisamarDetalhe {
  radios_operantes: number;
  radios_inoperantes: number;
  baterias: number;
  carregadores: number;
  eots_disponiveis: string | null;
  eots_avariados: string | null;
}
export interface TeconDetalhe {
  houve_atendimento: boolean;
  carga_mal_posicionada?: boolean | null;
  carga_mal_posicionada_descricao?: string | null;
  area1_atendida?: boolean | null;
  area1_inicio?: string | null;
  area1_termino?: string | null;
  area2_atendida?: boolean | null;
  area2_inicio?: string | null;
  area2_termino?: string | null;
}
export interface PassagemBase {
  data: string;
  turma: Turma;
  turno: Turno;
  observacoes: string | null;
  relatorio_ocorrencias: string | null;
  mobile_utilizado: boolean;
  mobile_justificativa: string | null;
  equipe: EquipeMembro[];
  ocupacoes_linhas: LinhaOcupacao[];
  radios_utilizados: RadioUso[];
}
export interface PassagemConsulta extends PassagemBase {
  id: string;
  terminal: Terminal;
  detalhe: BrisamarDetalhe | TeconDetalhe;
  editavel: boolean;
}
export type PassagemPayload = PassagemBase & {
  detalhe: BrisamarDetalhe | TeconDetalhe;
};
export interface PassagemResultado {
  id: string;
  mensagem: string;
  ciclo_id?: string | null;
  terminal_pendente?: Terminal | null;
}
export interface CicloPassagem {
  id: string;
  data: string;
  turma: Turma;
  turno: Turno;
  estado: 'RASCUNHO' | 'CONFIRMADO';
  confirmado_em: string | null;
  terminal_pendente: Terminal | null;
  passagens: PassagemConsulta[];
}
export interface CicloConsultaItem extends CicloPassagem {
  responsavel: {
    nome: string;
    matricula: string;
  };
}
export interface CicloConsultaFiltros {
  data_inicio?: string;
  data_fim?: string;
  turma?: Turma;
  turno?: Turno;
  responsavel?: string;
  protocolo?: string;
  pagina?: number;
  por_pagina?: number;
}
export interface CicloConsultaLista {
  itens: CicloConsultaItem[];
  paginacao: {
    pagina: number;
    por_pagina: number;
    total_itens: number;
    total_paginas: number;
  };
}
export interface PassagemHistoricoItem {
  versao: number;
  alterado_em: string;
  alterador: {
    nome: string;
    matricula: string;
  };
  snapshot: Record<string, unknown>;
}
export interface PassagemHistoricoLista {
  passagem_atual: PassagemConsulta;
  itens: PassagemHistoricoItem[];
  paginacao: {
    pagina: number;
    por_pagina: number;
    total_itens: number;
    total_paginas: number;
  };
}
export interface UltimaPassagem extends PassagemResultado {
  operacao: 'criacao' | 'edicao';
  terminal: 'Pátio Brisamar' | 'Terminal TECON';
  data: string;
  turma: Turma;
  turno: Turno;
}
