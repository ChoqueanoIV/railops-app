import { apiClient } from '@/services/api/client';
import type {
  CicloPassagem,
  CicloConsultaFiltros,
  CicloConsultaLista,
  PassagemConsulta,
  PassagemHistoricoLista,
  PassagemPayload,
  PassagemResultado,
  Terminal,
} from './types';

export const passagemService = {
  listar: (filtros: CicloConsultaFiltros) => {
    const parametros = new URLSearchParams();
    Object.entries(filtros).forEach(([chave, valor]) => {
      if (valor !== undefined && valor !== '') {
        parametros.set(chave, String(valor));
      }
    });
    return apiClient.request<CicloConsultaLista>(
      `/passagens/ciclos?${parametros}`,
    );
  },
  consultar: (id: string) =>
    apiClient.request<PassagemConsulta>(`/passagens/${id}`),
  consultarHistorico: (id: string, pagina = 1) =>
    apiClient.request<PassagemHistoricoLista>(
      `/passagens/${id}/historico?pagina=${pagina}&por_pagina=20`,
    ),
  consultarCiclo: (id: string) =>
    apiClient.request<CicloPassagem>(`/passagens/ciclos/${id}`),
  recuperarRascunho: (data: string, turma: string, turno: string) =>
    apiClient.request<CicloPassagem>(
      `/passagens/ciclos/rascunho?${new URLSearchParams({ data, turma, turno })}`,
    ),
  confirmarCiclo: (id: string) =>
    apiClient.request<CicloPassagem>(`/passagens/ciclos/${id}/confirmar`, {
      method: 'POST',
    }),
  salvar: (terminal: Terminal, payload: PassagemPayload, id?: string) => {
    const body: Partial<PassagemPayload> = { ...payload };
    if (id) {
      delete body.data;
      delete body.turma;
      delete body.turno;
    }
    return apiClient.request<PassagemResultado>(
      id ? `/passagens/${id}` : `/passagens/${terminal.toLowerCase()}`,
      {
        method: id ? 'PUT' : 'POST',
        body: JSON.stringify(body),
      },
    );
  },
};
