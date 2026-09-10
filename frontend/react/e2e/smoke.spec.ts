import { expect, test } from '@playwright/test';

test('redireciona visitante sem sessão para o login', async ({ page }) => {
  await page.goto('/');

  await expect(
    page.getByRole('heading', { name: 'Acessar a passagem digital' }),
  ).toBeVisible();
  await expect(page).toHaveURL(/\/login$/);
});
