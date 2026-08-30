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
  afterEach(() => vi.unstubAllGlobals());

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
