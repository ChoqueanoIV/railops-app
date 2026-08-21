import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it } from 'vitest';

import { App } from '@/app/App';

describe('shell React', () => {
  it('apresenta o RailOps e informa que o legado continua disponível', () => {
    render(
      <MemoryRouter>
        <App />
      </MemoryRouter>,
    );

    expect(screen.getByRole('heading', { name: 'RailOps' })).toBeVisible();
    expect(
      screen.getByText(/frontend legado durante a migração/i),
    ).toBeVisible();
  });

  it('redireciona rotas desconhecidas para o shell', () => {
    render(
      <MemoryRouter initialEntries={['/rota-inexistente']}>
        <App />
      </MemoryRouter>,
    );

    expect(screen.getByRole('heading', { name: 'RailOps' })).toBeVisible();
  });
});
