import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it } from 'vitest';

import { App } from '@/app/App';

describe('shell React', () => {
  it('redireciona uma sessão ausente para o login', () => {
    render(
      <MemoryRouter initialEntries={['/terminal']}>
        <App />
      </MemoryRouter>,
    );

    expect(
      screen.getByRole('heading', { name: 'Acessar o RailOps' }),
    ).toBeVisible();
  });

  it('apresenta o shell para uma sessão autenticada', () => {
    sessionStorage.setItem('access_token', 'jwt-de-teste');

    render(
      <MemoryRouter initialEntries={['/terminal']}>
        <App />
      </MemoryRouter>,
    );

    expect(
      screen.getByRole('heading', { name: 'Selecione o terminal' }),
    ).toBeVisible();
    expect(screen.getByRole('link', { name: /Pátio Brisamar/i })).toBeVisible();
    expect(screen.getByRole('link', { name: /Terminal TECON/i })).toBeVisible();
    expect(
      screen.getByRole('link', { name: 'Consultar passagens' }),
    ).toHaveAttribute('href', '/passagens');
  });

  it('encerra a sessão sem expor o token', async () => {
    const user = userEvent.setup();
    sessionStorage.setItem('access_token', 'jwt-de-teste');

    render(
      <MemoryRouter initialEntries={['/terminal']}>
        <App />
      </MemoryRouter>,
    );

    await user.click(screen.getByRole('button', { name: 'Sair' }));

    expect(
      await screen.findByRole('heading', { name: 'Acessar o RailOps' }),
    ).toBeVisible();
    expect(sessionStorage.getItem('access_token')).toBeNull();
  });
});
