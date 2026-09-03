import { expect, test } from '@playwright/test';
import { autenticar, MANOBRADOR } from './support/ciclo';

test('remove a sessão inválida após 401 e retorna ao login sem expor credenciais', async ({
  page,
}) => {
  await autenticar(page, MANOBRADOR);
  const tokenInvalido = 'jwt-e2e-expirado-e-invalido';
  await page.evaluate(
    (token) => sessionStorage.setItem('access_token', token),
    tokenInvalido,
  );

  const resposta401 = page.waitForResponse(
    (resposta) =>
      resposta.url().includes('/passagens/ciclos?') &&
      resposta.status() === 401,
  );
  await page.goto('/passagens');
  await resposta401;

  await expect(
    page.getByRole('heading', { name: 'Acessar o RailOps' }),
  ).toBeVisible();
  await expect(page).toHaveURL(/\/login$/);
  expect(
    await page.evaluate(() => sessionStorage.getItem('access_token')),
  ).toBeNull();
  expect(page.url()).not.toContain(tokenInvalido);
  await expect(page.locator('body')).not.toContainText(tokenInvalido);
  await expect(page.locator('body')).not.toContainText(MANOBRADOR.pin);
  await expect(page.locator('body')).not.toContainText(MANOBRADOR.matricula);
});
