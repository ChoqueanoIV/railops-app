import { apiClient } from '@/services/api/client';
import type {
  CicloPassagem,
  PassagemConsulta,
  PassagemPayload,
  PassagemResultado,
  Terminal,
} from './types';

export const passagemService = {
  consultar: (id: string) =>
    apiClient.request<PassagemConsulta>(`/passagens/${id}`),
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
