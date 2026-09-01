import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { App } from '@/app/App';

describe('migração das passagens para React', () => {
  beforeEach(() => sessionStorage.setItem('access_token', 'jwt-de-teste'));
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it('permite registrar separadamente os lados e travessões de L22 e L24', () => {
    render(
      <MemoryRouter initialEntries={['/brisamar']}>
        <App />
      </MemoryRouter>,
    );
    expect(
      screen.getByRole('heading', { name: 'Nova passagem de serviço' }),
    ).toBeVisible();
    expect(screen.getByLabelText('Veículos da linha 16')).toBeVisible();
    expect(screen.getByLabelText('Veículos da linha 22 SUP')).toBeVisible();
    expect(screen.getByLabelText('Veículos da linha 22 INF')).toBeVisible();
    expect(
      screen.getByLabelText('Veículos da linha Travessão L22'),
    ).toBeVisible();
    expect(screen.getByLabelText('Veículos da linha 24 SUP')).toBeVisible();
    expect(screen.getByLabelText('Veículos da linha 24 INF')).toBeVisible();
    expect(
      screen.getByLabelText('Veículos da linha Travessão L24'),
    ).toBeVisible();
    expect(screen.queryByText('Posição')).not.toBeInTheDocument();
  });

  it('mostra apenas os detalhes aplicáveis ao atendimento TECON', async () => {
    const user = userEvent.setup();
    render(
      <MemoryRouter initialEntries={['/tecon']}>
        <App />
      </MemoryRouter>,
    );
    expect(
      screen.queryByText('Havia carga mal posicionada?'),
    ).not.toBeInTheDocument();
    const grupo = screen.getByRole('group', { name: 'Houve atendimento?' });
    await user.click(withinGroup(grupo, 'Sim'));
    expect(screen.getByText('Havia carga mal posicionada?')).toBeVisible();
    expect(
      screen.getByLabelText('Veículos da linha Viaduto/DM1A'),
    ).toBeVisible();
  });

  it('protege também as novas rotas sem sessão', () => {
    sessionStorage.clear();
    render(
      <MemoryRouter initialEntries={['/brisamar']}>
        <App />
      </MemoryRouter>,
    );
    expect(
      screen.getByRole('heading', { name: 'Acessar o RailOps' }),
    ).toBeVisible();
  });

  it('recupera do servidor a revisão completa dos dois terminais', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify(cicloCompleto()), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }),
      ),
    );
    render(
      <MemoryRouter initialEntries={['/confirmacao?ciclo=ciclo-1']}>
        <App />
      </MemoryRouter>,
    );

    expect(
      await screen.findByRole('heading', { name: 'Passagem completa' }),
    ).toBeVisible();
    expect(
      screen.getByRole('heading', { name: 'Pátio Brisamar' }),
    ).toBeVisible();
    expect(
      screen.getByRole('heading', { name: 'Terminal TECON' }),
    ).toBeVisible();
    expect(
      screen.getByRole('button', { name: 'Confirmar passagem completa' }),
    ).toBeEnabled();
  });

  it('baixa o PDF individual somente após a confirmação', async () => {
    const user = userEvent.setup();
    const ciclo = cicloCompleto('CONFIRMADO');
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(
        new Response(JSON.stringify(ciclo), {
          headers: { 'Content-Type': 'application/json' },
        }),
      )
      .mockResolvedValueOnce(
        new Response('pdf', {
          headers: {
            'Content-Type': 'application/pdf',
            'Content-Disposition': 'attachment; filename="passagem.pdf"',
          },
        }),
      );
    vi.stubGlobal('fetch', fetchMock);
    vi.stubGlobal('URL', {
      ...URL,
      createObjectURL: vi.fn(() => 'blob:pdf'),
      revokeObjectURL: vi.fn(),
    });
    vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {});

    render(
      <MemoryRouter initialEntries={['/confirmacao?ciclo=ciclo-1']}>
        <App />
      </MemoryRouter>,
    );
    await user.click(await screen.findByRole('button', { name: 'Baixar PDF' }));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    expect(String(fetchMock.mock.calls[1][0])).toContain(
      '/passagens/ciclos/ciclo-1/exportacao.pdf',
    );
  });
});

function cicloCompleto(estado: 'RASCUNHO' | 'CONFIRMADO' = 'RASCUNHO') {
  const base = {
    data: '2026-08-30',
    turma: 'C',
    turno: 'DIURNO',
    observacoes: 'Sem alterações',
    relatorio_ocorrencias: 'Sem ocorrências',
    mobile_utilizado: true,
    mobile_justificativa: null,
    equipe: [{ nome: 'Operador', matricula: '12345678' }],
    ocupacoes_linhas: [],
    radios_utilizados: [],
    editavel: estado === 'RASCUNHO',
  };
  return {
    id: 'ciclo-1',
    data: '2026-08-30',
    turma: 'C',
    turno: 'DIURNO',
    estado,
    confirmado_em: estado === 'CONFIRMADO' ? '2026-08-30T21:50:00Z' : null,
    terminal_pendente: null,
    passagens: [
      {
        ...base,
        id: 'brisamar-1',
        terminal: 'BRISAMAR',
        detalhe: {
          radios_operantes: 4,
          radios_inoperantes: 0,
          baterias: 4,
          carregadores: 2,
          eots_disponiveis: null,
          eots_avariados: null,
        },
      },
      {
        ...base,
        id: 'tecon-1',
        terminal: 'TECON',
        detalhe: { houve_atendimento: false },
      },
    ],
  };
}

function withinGroup(group: HTMLElement, name: string) {
  const input = Array.from(group.querySelectorAll('input')).find((item) =>
    item.parentElement?.textContent?.includes(name),
  );
  if (!input) throw new Error(`Opção ${name} não encontrada.`);
  return input;
}
