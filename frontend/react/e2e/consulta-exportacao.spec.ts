import { expect, test } from '@playwright/test';
import {
  autenticar,
  INSTRUTOR,
  prepararCicloConfirmado,
} from './support/ciclo';

test('localiza o ciclo confirmado e baixa o PDF individual autenticado', async ({
  page,
  request,
}) => {
  const { data, cicloId } = await prepararCicloConfirmado(request);
  await autenticar(page, INSTRUTOR);

  await page.getByRole('link', { name: 'Consultar passagens' }).click();
  await expect(
    page.getByRole('heading', { name: 'Consultar passagens' }),
  ).toBeVisible();
  await page.getByLabel('Data inicial').fill(data);
  await page.getByLabel('Data final').fill(data);
  await page.getByLabel('Turma').selectOption(INSTRUTOR.turma);
  await page.getByLabel('Responsável').fill(INSTRUTOR.matricula);
  await page.getByRole('button', { name: 'Aplicar filtros' }).click();

  const resultado = page.locator('article').filter({ hasText: cicloId });
  await expect(resultado).toContainText('Instrutor E2E');
  await expect(resultado).toContainText(`Matrícula ${INSTRUTOR.matricula}`);
  await resultado.getByRole('link', { name: 'Ver passagem completa' }).click();
  await expect(page.getByText('Confirmado — somente leitura')).toBeVisible();

  const token = await page.evaluate(() =>
    sessionStorage.getItem('access_token'),
  );
  expect(token).toBeTruthy();
  const respostaPromise = page.waitForResponse((resposta) =>
    resposta.url().includes(`/passagens/ciclos/${cicloId}/exportacao.pdf`),
  );
  const downloadPromise = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Baixar PDF' }).click();
  const [resposta, download] = await Promise.all([
    respostaPromise,
    downloadPromise,
  ]);

  expect(resposta.status()).toBe(200);
  expect(resposta.headers()['content-type']).toContain('application/pdf');
  expect(resposta.headers()['content-disposition']).toContain('.pdf');
  expect(download.suggestedFilename()).toBe(
    `railops-passagem-${data}-${cicloId}.pdf`,
  );
  const stream = await download.createReadStream();
  const partes: Buffer[] = [];
  for await (const parte of stream) {
    partes.push(Buffer.isBuffer(parte) ? parte : Buffer.from(parte));
  }
  const conteudo = Buffer.concat(partes);
  expect(conteudo.length).toBeGreaterThan(1_000);
  expect(conteudo.subarray(0, 5).toString()).toBe('%PDF-');
  expect(resposta.url()).not.toContain(token!);
  expect(new URL(resposta.url()).search).toBe('');
});
