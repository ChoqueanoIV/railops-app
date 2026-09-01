import { expect, test, type Page } from '@playwright/test';

const MATRICULA = '91000002';
const PIN = '1234';

test('preenche os dois terminais, revisa e bloqueia o ciclo confirmado', async ({
  page,
}) => {
  await autenticar(page);
  await page.getByRole('link', { name: /Pátio Brisamar/ }).click();

  const operacao = await obterOperacaoAtual(page);
  await page.getByLabel('Data').fill(operacao.data);
  await page.getByLabel('Turma').selectOption('C');
  await page.getByLabel('Turno').selectOption(operacao.turno);
  await preencherEquipe(page, 'Manobrador E2E Brisamar');
  await page.getByLabel('Veículos da linha 22 SUP').fill('Vagões SUP E2E');
  await page.getByLabel('Veículos da linha 22 INF').fill('Vagões INF E2E');
  await page
    .getByLabel('Veículos da linha Travessão L22')
    .fill('Travessão L22 E2E');
  await page.getByLabel('Veículos da linha 24 SUP').fill('Vagões SUP L24 E2E');
  await page.getByLabel('Veículos da linha 24 INF').fill('Vagões INF L24 E2E');
  await page
    .getByLabel('Veículos da linha Travessão L24')
    .fill('Travessão L24 E2E');
  await page.getByLabel('Observações').fill('Brisamar revisado no E2E');
  await page
    .getByRole('button', { name: 'Enviar passagem de serviço' })
    .click();

  await expect(page).toHaveURL(/\/tecon\?ciclo=/);
  await preencherEquipe(page, 'Manobrador E2E TECON');
  await page.getByLabel('Veículos da linha L1').fill('Composição TECON E2E');
  await page.getByLabel('Observações').fill('TECON revisado no E2E');
  await page
    .getByLabel('Relatório de ocorrências')
    .fill('Sem ocorrências no TECON');
  await page
    .getByRole('button', { name: 'Enviar passagem de serviço' })
    .click();

  await expect(page).toHaveURL(/\/confirmacao\?ciclo=/);
  await expect(
    page.getByRole('heading', { name: 'Passagem completa' }),
  ).toBeVisible();
  await expect(
    page.getByRole('heading', { name: 'Pátio Brisamar' }),
  ).toBeVisible();
  await expect(
    page.getByRole('heading', { name: 'Terminal TECON' }),
  ).toBeVisible();
  await expect(page.getByText('Vagões SUP E2E')).toBeVisible();
  await expect(page.getByText('Vagões INF E2E')).toBeVisible();
  await expect(page.getByText('Travessão L22 E2E')).toBeVisible();
  await expect(page.getByText('Travessão L24 E2E')).toBeVisible();
  await expect(page.getByText('Composição TECON E2E')).toBeVisible();

  const correcaoBrisamar = await page
    .getByRole('link', { name: 'Corrigir Pátio Brisamar' })
    .getAttribute('href');
  expect(correcaoBrisamar).toBeTruthy();

  await page
    .getByRole('button', { name: 'Confirmar passagem completa' })
    .click();
  await expect(page.getByText('Confirmado — somente leitura')).toBeVisible();
  await expect(
    page.getByText(/Brisamar e TECON estão bloqueados para edição/),
  ).toBeVisible();
  await expect(page.getByRole('link', { name: /^Corrigir / })).toHaveCount(0);

  await page.reload();
  await expect(page.getByText('Confirmado — somente leitura')).toBeVisible();
  await expect(page.getByRole('link', { name: /^Corrigir / })).toHaveCount(0);

  await page.goto(correcaoBrisamar!);
  await expect(page.getByRole('alert')).toHaveText(
    'Esta passagem não pode mais ser editada.',
  );
});

async function autenticar(page: Page) {
  await page.goto('/login');
  await page.getByLabel('Matrícula').fill(MATRICULA);
  await page.getByLabel('PIN', { exact: true }).fill(PIN);
  await page.getByRole('button', { name: 'Entrar' }).click();
  await expect(
    page.getByRole('heading', { name: 'Selecione o terminal' }),
  ).toBeVisible();
}

async function preencherEquipe(page: Page, nome: string) {
  await page.getByLabel('Nome').fill(nome);
  await page.getByLabel('Matrícula (8 dígitos)').fill(MATRICULA);
}

async function obterOperacaoAtual(
  page: Page,
): Promise<{ data: string; turno: 'DIURNO' | 'NOTURNO' }> {
  return page.evaluate(() => {
    const agora = new Date();
    const partes = new Intl.DateTimeFormat('en-CA', {
      timeZone: 'America/Sao_Paulo',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      hourCycle: 'h23',
    }).formatToParts(agora);
    const valor = (tipo: Intl.DateTimeFormatPartTypes) =>
      partes.find((parte) => parte.type === tipo)?.value ?? '';
    const data = `${valor('year')}-${valor('month')}-${valor('day')}`;
    const hora = Number(valor('hour'));
    if (hora >= 7 && hora < 19) return { data, turno: 'DIURNO' };
    if (hora >= 19) return { data, turno: 'NOTURNO' };

    const diaAnterior = new Date(`${data}T12:00:00-03:00`);
    diaAnterior.setDate(diaAnterior.getDate() - 1);
    const dataAnterior = new Intl.DateTimeFormat('en-CA', {
      timeZone: 'America/Sao_Paulo',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
    }).format(diaAnterior);
    return { data: dataAnterior, turno: 'NOTURNO' };
  });
}
