import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { App } from '@/app/App';

const resposta = (itens = [cicloConfirmado()]) =>
  new Response(
    JSON.stringify({
      itens,
      paginacao: {
        pagina: 1,
        por_pagina: 20,
        total_itens: itens.length,
        total_paginas: itens.length ? 1 : 0,
      },
    }),
    { status: 200, headers: { 'Content-Type': 'application/json' } },
  );

describe('consulta de passagens', () => {
  beforeEach(() => sessionStorage.setItem('access_token', 'jwt-de-teste'));
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it('lista o ciclo completo com responsável e acesso ao detalhe', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(resposta()));

    render(
      <MemoryRouter initialEntries={['/passagens']}>
        <App />
      </MemoryRouter>,
    );

    expect(
      await screen.findByRole('heading', { name: 'Responsável de Teste' }),
    ).toBeVisible();
    expect(screen.getByText('Matrícula 30032552')).toBeVisible();
    expect(screen.getByText('ciclo-1')).toBeVisible();
    expect(
      screen.getByRole('link', { name: 'Ver passagem completa' }),
    ).toHaveAttribute('href', '/confirmacao?ciclo=ciclo-1');
  });

  it('aplica filtros e mantém a paginação no servidor', async () => {
    const user = userEvent.setup();
    const fetchMock = vi.fn().mockResolvedValue(resposta());
    vi.stubGlobal('fetch', fetchMock);

    render(
      <MemoryRouter initialEntries={['/passagens']}>
        <App />
      </MemoryRouter>,
    );
    await screen.findByText('1 passagem(ns) encontrada(s)');

    await user.selectOptions(screen.getByLabelText('Turma'), 'C');
    await user.selectOptions(screen.getByLabelText('Turno'), 'NOTURNO');
    await user.type(screen.getByLabelText('Responsável'), '30032552');
    await user.click(screen.getByRole('button', { name: 'Aplicar filtros' }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    const url = String(fetchMock.mock.calls[1][0]);
    expect(url).toContain('turma=C');
    expect(url).toContain('turno=NOTURNO');
    expect(url).toContain('responsavel=30032552');
    expect(url).toContain('pagina=1');
    expect(url).toContain('por_pagina=20');
  });

  it('informa quando o período não possui passagens', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(resposta([])));

    render(
      <MemoryRouter initialEntries={['/passagens']}>
        <App />
      </MemoryRouter>,
    );

    expect(
      await screen.findByText('Nenhuma passagem encontrada neste período.'),
    ).toBeVisible();
  });

  it('exporta CSV com filtros ativos e token somente no cabeçalho', async () => {
    const user = userEvent.setup();
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(resposta())
      .mockResolvedValueOnce(
        new Response('csv', {
          headers: {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename="passagens.csv"',
          },
        }),
      );
    vi.stubGlobal('fetch', fetchMock);
    vi.stubGlobal('URL', {
      ...URL,
      createObjectURL: vi.fn(() => 'blob:arquivo'),
      revokeObjectURL: vi.fn(),
    });
    vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {});

    render(
      <MemoryRouter initialEntries={['/passagens']}>
        <App />
      </MemoryRouter>,
    );
    await screen.findByText('1 passagem(ns) encontrada(s)');
    await user.selectOptions(screen.getByLabelText('Turma'), 'C');
    await user.click(screen.getByRole('button', { name: 'Aplicar filtros' }));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    fetchMock.mockResolvedValueOnce(
      new Response('csv', {
        headers: {
          'Content-Type': 'text/csv',
          'Content-Disposition': 'attachment; filename="passagens.csv"',
        },
      }),
    );
    await user.click(screen.getByRole('button', { name: 'Exportar CSV' }));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(3));

    const [url, init] = fetchMock.mock.calls[2];
    expect(String(url)).toContain('/passagens/ciclos/exportacoes.csv?');
    expect(String(url)).toContain('turma=C');
    expect(String(url)).not.toContain('pagina=');
    expect(String(url)).not.toContain('jwt-de-teste');
    expect(new Headers(init.headers).get('Authorization')).toBe(
      'Bearer jwt-de-teste',
    );
  });

  it('informa bloqueio de perfil sem encerrar a sessão', async () => {
    const user = userEvent.setup();
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(resposta())
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            error: {
              code: 'SPECIAL_ACCESS_DENIED',
              message: 'Sem permissão.',
              details: null,
            },
          }),
          { status: 403, headers: { 'Content-Type': 'application/json' } },
        ),
      );
    vi.stubGlobal('fetch', fetchMock);

    render(
      <MemoryRouter initialEntries={['/passagens']}>
        <App />
      </MemoryRouter>,
    );
    await screen.findByText('1 passagem(ns) encontrada(s)');
    await user.click(screen.getByRole('button', { name: 'Exportar PDF' }));

    expect(
      await screen.findByText(
        'Seu perfil não possui permissão para exportações consolidadas.',
      ),
    ).toBeVisible();
    expect(sessionStorage.getItem('access_token')).toBe('jwt-de-teste');
  });

  it('protege a rota quando não existe sessão', () => {
    sessionStorage.clear();

    render(
      <MemoryRouter initialEntries={['/passagens']}>
        <App />
      </MemoryRouter>,
    );

    expect(
      screen.getByRole('heading', { name: 'Acessar o RailOps' }),
    ).toBeVisible();
  });
});

function cicloConfirmado() {
  return {
    id: 'ciclo-1',
    data: '2026-08-30',
    turma: 'C',
    turno: 'DIURNO',
    estado: 'CONFIRMADO',
    confirmado_em: '2026-08-30T21:50:00Z',
    terminal_pendente: null,
    responsavel: { nome: 'Responsável de Teste', matricula: '30032552' },
    passagens: [],
  };
}
