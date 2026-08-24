import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import { beforeEach, describe, expect, it } from 'vitest';
import { App } from '@/app/App';

describe('migração das passagens para React', () => {
  beforeEach(() => sessionStorage.setItem('access_token', 'jwt-de-teste'));

  it('mantém as linhas e a posição obrigatória do Brisamar', () => {
    render(
      <MemoryRouter initialEntries={['/brisamar']}>
        <App />
      </MemoryRouter>,
    );
    expect(
      screen.getByRole('heading', { name: 'Nova passagem de serviço' }),
    ).toBeVisible();
    expect(screen.getByLabelText('Veículos da linha 16')).toBeVisible();
    expect(screen.getByLabelText('Posição da linha 22')).toBeRequired();
    expect(
      screen.queryByLabelText('Posição da linha 16'),
    ).not.toBeInTheDocument();
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
});

function withinGroup(group: HTMLElement, name: string) {
  const input = Array.from(group.querySelectorAll('input')).find((item) =>
    item.parentElement?.textContent?.includes(name),
  );
  if (!input) throw new Error(`Opção ${name} não encontrada.`);
  return input;
}
