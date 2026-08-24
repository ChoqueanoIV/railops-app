import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';

import { App } from '@/app/App';

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

async function fillLogin(user: ReturnType<typeof userEvent.setup>) {
  await user.type(screen.getByLabelText('Matrícula'), '30032552');
  await user.type(screen.getByLabelText('PIN'), '4321');
}

describe('autenticação React', () => {
  it('autentica pelo contrato existente e abre a rota protegida', async () => {
    const user = userEvent.setup();
    const fetchMock = vi
      .spyOn(window, 'fetch')
      .mockResolvedValue(
        jsonResponse({ access_token: 'jwt-valido', token_type: 'bearer' }),
      );

    render(
      <MemoryRouter initialEntries={['/login']}>
        <App />
      </MemoryRouter>,
    );

    await fillLogin(user);
    await user.click(screen.getByRole('button', { name: 'Entrar' }));

    expect(
      await screen.findByRole('heading', { name: 'Selecione o terminal' }),
    ).toBeVisible();
    expect(sessionStorage.getItem('access_token')).toBe('jwt-valido');
    expect(fetchMock).toHaveBeenCalledWith(
      'http://127.0.0.1:8000/auth/login',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ matricula: '30032552', pin: '4321' }),
      }),
    );
  });

  it('exibe de forma controlada o erro retornado pela API', async () => {
    const user = userEvent.setup();
    vi.spyOn(window, 'fetch').mockResolvedValue(
      jsonResponse(
        {
          detail: 'Matrícula ou PIN inválidos.',
          error: {
            code: 'INVALID_CREDENTIALS',
            message: 'Matrícula ou PIN inválidos.',
            details: null,
          },
        },
        401,
      ),
    );

    render(
      <MemoryRouter initialEntries={['/login']}>
        <App />
      </MemoryRouter>,
    );

    await fillLogin(user);
    await user.click(screen.getByRole('button', { name: 'Entrar' }));

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Matrícula ou PIN inválidos.',
    );
    expect(sessionStorage.getItem('access_token')).toBeNull();
  });

  it('valida a confirmação antes do primeiro acesso', async () => {
    const user = userEvent.setup();
    const fetchMock = vi.spyOn(window, 'fetch');

    render(
      <MemoryRouter initialEntries={['/login']}>
        <App />
      </MemoryRouter>,
    );

    await user.click(screen.getByRole('button', { name: /primeiro acesso/i }));
    await user.type(screen.getByLabelText('Matrícula'), '30032552');
    await user.type(screen.getByLabelText('Código de ativação'), '123456');
    await user.type(screen.getByLabelText('Novo PIN'), '4321');
    await user.type(screen.getByLabelText('Confirmar novo PIN'), '1234');
    await user.click(screen.getByRole('button', { name: 'Definir meu PIN' }));

    expect(screen.getByRole('alert')).toHaveTextContent(
      'O PIN e a confirmação não coincidem.',
    );
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it('conclui o primeiro acesso e retorna ao login', async () => {
    const user = userEvent.setup();
    vi.spyOn(window, 'fetch').mockResolvedValue(
      jsonResponse({ mensagem: 'PIN definido com sucesso' }, 201),
    );

    render(
      <MemoryRouter initialEntries={['/login']}>
        <App />
      </MemoryRouter>,
    );

    await user.click(screen.getByRole('button', { name: /primeiro acesso/i }));
    await user.type(screen.getByLabelText('Matrícula'), '30032552');
    await user.type(screen.getByLabelText('Código de ativação'), '123456');
    await user.type(screen.getByLabelText('Novo PIN'), '4321');
    await user.type(screen.getByLabelText('Confirmar novo PIN'), '4321');
    await user.click(screen.getByRole('button', { name: 'Definir meu PIN' }));

    expect(
      await screen.findByRole('heading', { name: 'Acessar o RailOps' }),
    ).toBeVisible();
    expect(screen.getByRole('alert')).toHaveTextContent(
      'PIN definido com sucesso. Agora você pode entrar.',
    );
  });
});
