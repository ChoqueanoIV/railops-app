import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { App } from '@/app/App';

const responder = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });

describe('histórico auditável da passagem', () => {
  beforeEach(() => sessionStorage.setItem('access_token', 'jwt-valido'));
  afterEach(() => vi.unstubAllGlobals());

  it('mostra autor e compara o estado anterior com o estado final', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(responder(historico())));

    render(
      <MemoryRouter initialEntries={['/passagens/passagem-1/historico']}>
        <App />
      </MemoryRouter>,
    );

    expect(
      await screen.findByRole('heading', { name: 'Versão 1' }),
    ).toBeVisible();
    expect(screen.getByText('Instrutora Teste · 87654321')).toBeVisible();
    expect(screen.getByText('Antes da correção')).toBeVisible();
    expect(screen.getByText('Estado final')).toBeVisible();
  });

  it('explica a falta de permissão e mantém a sessão do manobrador', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        responder(
          {
            error: {
              code: 'HISTORY_ACCESS_DENIED',
              message: 'Usuário sem permissão para consultar o histórico.',
              details: null,
            },
          },
          403,
        ),
      ),
    );

    render(
      <MemoryRouter initialEntries={['/passagens/passagem-1/historico']}>
        <App />
      </MemoryRouter>,
    );

    expect(
      await screen.findByText(
        'Seu perfil não possui permissão para consultar o histórico de edições.',
      ),
    ).toBeVisible();
    expect(sessionStorage.getItem('access_token')).toBe('jwt-valido');
  });
});

function historico() {
  return {
    passagem_atual: {
      id: 'passagem-1',
      terminal: 'BRISAMAR',
      data: '2026-08-30',
      turma: 'C',
      turno: 'DIURNO',
      observacoes: 'Estado final',
      relatorio_ocorrencias: null,
      mobile_utilizado: true,
      mobile_justificativa: null,
      equipe: [],
      ocupacoes_linhas: [],
      detalhe: {
        radios_operantes: 4,
        radios_inoperantes: 0,
        baterias: 4,
        carregadores: 2,
        eots_disponiveis: null,
        eots_avariados: null,
      },
      radios_utilizados: [],
      editavel: false,
    },
    itens: [
      {
        versao: 1,
        alterado_em: '2026-08-30T18:45:00Z',
        alterador: { nome: 'Instrutora Teste', matricula: '87654321' },
        snapshot: {
          passagem: {
            observacoes: 'Antes da correção',
            relatorio_ocorrencias: null,
            mobile_utilizado: true,
            mobile_justificativa: null,
          },
          detalhe: {
            radios_operantes: 4,
            radios_inoperantes: 0,
            baterias: 4,
            carregadores: 2,
            eots_disponiveis: null,
            eots_avariados: null,
          },
          equipe: [],
          ocupacoes_linhas: [],
          radios_utilizados: [],
        },
      },
    ],
    paginacao: {
      pagina: 1,
      por_pagina: 20,
      total_itens: 1,
      total_paginas: 1,
    },
  };
}
