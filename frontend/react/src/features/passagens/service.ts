import { apiClient } from '@/services/api/client';
import type {
  PassagemConsulta,
  PassagemPayload,
  PassagemResultado,
  Terminal,
} from './types';

export const passagemService = {
  consultar: (id: string) =>
    apiClient.request<PassagemConsulta>(`/passagens/${id}`),
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
