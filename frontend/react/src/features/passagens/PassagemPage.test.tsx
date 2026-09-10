import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { App } from '@/app/App';
import type { CicloPassagem } from './types';

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
      screen.getByRole('heading', { name: 'Nova passagem de turno' }),
    ).toBeVisible();
    expect(
      screen.getByRole('navigation', { name: 'Etapas do preenchimento' }),
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
    expect(screen.getByLabelText('Veículos da linha 16')).toBeRequired();
    expect(screen.getByLabelText('Linha 16 livre')).not.toBeChecked();
  });

  it('permite declarar uma linha livre ou exige a descrição da ocupação', async () => {
    const user = userEvent.setup();
    render(
      <MemoryRouter initialEntries={['/tecon']}>
        <App />
      </MemoryRouter>,
    );

    const ocupacao = screen.getByLabelText('Veículos da linha L1');
    await user.click(screen.getByLabelText('Linha L1 livre'));
    expect(ocupacao).toBeDisabled();
    expect(ocupacao).not.toBeRequired();

    await user.click(screen.getByLabelText('Linha L1 livre'));
    expect(ocupacao).toBeEnabled();
    expect(ocupacao).toBeRequired();
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

  it('torna os registros obrigatórios ou permite declarar ausência', async () => {
    const user = userEvent.setup();
    render(
      <MemoryRouter initialEntries={['/brisamar']}>
        <App />
      </MemoryRouter>,
    );

    const observacoes = screen.getByLabelText('Observações');
    const ocorrencias = screen.getByLabelText('Relatório de ocorrências');
    expect(observacoes).toBeRequired();
    expect(ocorrencias).toBeRequired();

    await user.click(screen.getByLabelText('Sem observações'));
    await user.click(screen.getByLabelText('Sem alterações'));
    expect(observacoes).toBeDisabled();
    expect(ocorrencias).toBeDisabled();
  });

  it('exige situação dos EOTs e declaração explícita quando nenhum rádio foi usado', async () => {
    const user = userEvent.setup();
    render(
      <MemoryRouter initialEntries={['/brisamar']}>
        <App />
      </MemoryRouter>,
    );

    const disponiveis = screen.getByLabelText('EOTs disponíveis');
    const avariados = screen.getByLabelText('EOTs avariados');
    const semRadios = screen.getByLabelText('Nenhum rádio utilizado');
    expect(disponiveis).toBeRequired();
    expect(avariados).toBeRequired();
    expect(semRadios).toBeRequired();

    await user.click(screen.getByLabelText('Nenhum EOT disponível'));
    await user.click(screen.getByLabelText('Nenhum EOT avariado'));
    await user.click(semRadios);
    expect(disponiveis).toBeDisabled();
    expect(avariados).toBeDisabled();
    expect(semRadios).toBeChecked();
  });

  it('converte textos digitados para maiúsculas e explica a inclusão na equipe', async () => {
    const user = userEvent.setup();
    render(
      <MemoryRouter initialEntries={['/brisamar']}>
        <App />
      </MemoryRouter>,
    );

    await user.type(screen.getByLabelText('Nome'), 'João da Silva');
    await user.type(screen.getByLabelText('Observações'), 'Pátio normal');
    await user.type(
      screen.getByLabelText('Veículos da linha 16'),
      'Vagões em teste',
    );
    await user.click(screen.getByRole('button', { name: 'Adicionar rádio' }));
    await user.click(screen.getByLabelText('Apresentou falha'));
    await user.type(
      screen.getByLabelText('Descrição da falha'),
      'Falha no botão',
    );
    expect(screen.getByLabelText('Nome')).toHaveValue('JOÃO DA SILVA');
    expect(screen.getByLabelText('Observações')).toHaveValue('PÁTIO NORMAL');
    expect(screen.getByLabelText('Veículos da linha 16')).toHaveValue(
      'VAGÕES EM TESTE',
    );
    expect(screen.getByLabelText('Descrição da falha')).toHaveValue(
      'FALHA NO BOTÃO',
    );
    expect(
      screen.getByRole('button', { name: 'Adicionar outro membro à equipe' }),
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
      screen.getByRole('heading', { name: 'Acessar a passagem digital' }),
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
    expect(screen.getByText('Não')).toBeVisible();
    expect(screen.queryByText('false')).not.toBeInTheDocument();
    expect(screen.queryByText('Não informado')).not.toBeInTheDocument();
  });

  it('oculta detalhes condicionais que não se aplicam ao atendimento', async () => {
    const ciclo = cicloCompleto();
    ciclo.passagens[1].detalhe = {
      houve_atendimento: true,
      carga_mal_posicionada: false,
      carga_mal_posicionada_descricao: null,
      area1_atendida: false,
      area1_inicio: null,
      area1_termino: null,
      area2_atendida: false,
      area2_inicio: null,
      area2_termino: null,
    };
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify(ciclo), {
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
      screen.queryByText('carga mal posicionada descricao'),
    ).not.toBeInTheDocument();
    expect(screen.queryByText('area1 inicio')).not.toBeInTheDocument();
    expect(screen.queryByText('area2 termino')).not.toBeInTheDocument();
  });

  it('bloqueia a confirmação de um rascunho antigo com campo vazio', async () => {
    const ciclo = cicloCompleto();
    ciclo.passagens[0].observacoes = '';
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify(ciclo), {
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
      await screen.findByText(
        'Existem campos pendentes. Corrija os terminais antes da confirmação final.',
      ),
    ).toBeVisible();
    expect(
      screen.getByRole('button', { name: 'Confirmar passagem completa' }),
    ).toBeDisabled();
    expect(screen.getByText('Pendente de correção')).toBeVisible();
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

function cicloCompleto(
  estado: 'RASCUNHO' | 'CONFIRMADO' = 'RASCUNHO',
): CicloPassagem {
  const base = {
    data: '2026-08-30',
    turma: 'C' as const,
    turno: 'DIURNO' as const,
    observacoes: 'Sem alterações',
    relatorio_ocorrencias: 'Sem ocorrências',
    mobile_utilizado: true,
    mobile_justificativa: null,
    equipe: [{ nome: 'Operador', matricula: '12345678' }],
    ocupacoes_linhas: [
      { codigo_linha: 'LINHA TESTE', veiculos: 'LIVRE', sup_inf: null },
    ],
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
          eots_disponiveis: 'NENHUM EOT DISPONÍVEL',
          eots_avariados: 'NENHUM EOT AVARIADO',
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
