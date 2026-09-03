import { expect, test } from '@playwright/test';

const MATRICULA = '91000001';
const CODIGO_ATIVACAO = '654321';
const NOVO_PIN = '4321';

test('ativa o primeiro acesso, autentica e protege o token', async ({
  page,
}) => {
  await page.goto('/login');

  await page
    .getByRole('button', { name: 'Primeiro acesso? Definir meu PIN' })
    .click();
  await page.getByLabel('Matrícula').fill(MATRICULA);
  await page.getByLabel('Código de ativação').fill(CODIGO_ATIVACAO);
  await page.getByLabel('Novo PIN', { exact: true }).fill(NOVO_PIN);
  await page.getByLabel('Confirmar novo PIN').fill(NOVO_PIN);
  await page.getByRole('button', { name: 'Definir meu PIN' }).click();

  await expect(page.getByRole('alert')).toHaveText(
    'PIN definido com sucesso. Agora você pode entrar.',
  );
  await page.getByLabel('PIN', { exact: true }).fill(NOVO_PIN);
  await page.getByRole('button', { name: 'Entrar' }).click();

  await expect(
    page.getByRole('heading', { name: 'Selecione o terminal' }),
  ).toBeVisible();
  await expect(
    page.getByRole('link', { name: /Pátio Brisamar/ }),
  ).toBeVisible();
  await expect(
    page.getByRole('link', { name: /Terminal TECON/ }),
  ).toBeVisible();
  await expect(page).toHaveURL(/\/terminal$/);

  const token = await page.evaluate(() =>
    sessionStorage.getItem('access_token'),
  );
  expect(token).toBeTruthy();
  expect(page.url()).not.toContain(token!);
  await expect(page.locator('body')).not.toContainText(token!);
});
