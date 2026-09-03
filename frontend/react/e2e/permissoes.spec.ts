import { expect, test, type Download, type Page } from '@playwright/test';
import {
  autenticar,
  type CredenciaisE2E,
  INSTRUTOR,
  MANOBRADOR,
  prepararCicloConfirmado,
} from './support/ciclo';

const CICLO_PERMISSOES: CredenciaisE2E = { ...INSTRUTOR, turma: 'A' };

test('aplica permissões sem encerrar a sessão e libera consolidados ao Instrutor', async ({
  page,
  request,
}) => {
  const { cicloId, passagemBrisamarId, data } = await prepararCicloConfirmado(
    request,
    CICLO_PERMISSOES,
  );

  await autenticar(page, MANOBRADOR);
  const tokenManobrador = await tokenDaSessao(page);
  await page.goto(`/passagens/${passagemBrisamarId}/historico`);
  await expect(page.getByRole('alert')).toContainText(
    'Seu perfil não possui permissão para consultar o histórico de edições.',
  );
  expect(await tokenDaSessao(page)).toBe(tokenManobrador);

  await page.goto('/passagens');
  await expect(
    page.getByRole('heading', { name: 'Consultar passagens' }),
  ).toBeVisible();
  for (const formato of ['CSV', 'PDF'] as const) {
    const resposta = page.waitForResponse(
      (item) =>
        item
          .url()
          .includes(`/passagens/ciclos/exportacoes.${formato.toLowerCase()}`) &&
        item.status() === 403,
    );
    await page.getByRole('button', { name: `Exportar ${formato}` }).click();
    await resposta;
    await expect(page.getByRole('alert')).toHaveText(
      'Seu perfil não possui permissão para exportações consolidadas.',
    );
    expect(await tokenDaSessao(page)).toBe(tokenManobrador);
  }
  await page.goto('/terminal');
  await expect(
    page.getByRole('heading', { name: 'Selecione o terminal' }),
  ).toBeVisible();
  await page.getByRole('button', { name: 'Sair' }).click();

  await autenticar(page, INSTRUTOR);
  await page.goto(`/passagens/${passagemBrisamarId}/historico`);
  await expect(
    page.getByRole('heading', { name: 'Histórico de edições' }),
  ).toBeVisible();
  await expect(
    page.getByText('Esta passagem ainda não possui edições.'),
  ).toBeVisible();

  await page.goto('/passagens');
  await page.getByLabel('Data inicial').fill(data);
  await page.getByLabel('Data final').fill(data);
  await page.getByLabel('Turma').selectOption(CICLO_PERMISSOES.turma);
  await page.getByRole('button', { name: 'Aplicar filtros' }).click();
  await expect(
    page.locator('article').filter({ hasText: cicloId }),
  ).toBeVisible();
  const tokenInstrutor = await tokenDaSessao(page);

  const csv = await baixarConsolidado(page, 'CSV');
  expect(csv.resposta.headers()['content-type']).toContain('text/csv');
  expect(csv.download.suggestedFilename()).toBe(
    `railops-passagens-${data}-${data}.csv`,
  );
  const textoCsv = csv.conteudo.toString('utf8');
  expect(textoCsv).toContain('protocolo');
  expect(textoCsv).toContain(cicloId);
  expect(textoCsv).not.toMatch(/access_token|codigo_ativacao|senha_hash/i);
  expect(csv.resposta.url()).not.toContain(tokenInstrutor);

  const pdf = await baixarConsolidado(page, 'PDF');
  expect(pdf.resposta.headers()['content-type']).toContain('application/pdf');
  expect(pdf.download.suggestedFilename()).toBe(
    `railops-passagens-${data}-${data}.pdf`,
  );
  expect(pdf.conteudo.length).toBeGreaterThan(1_000);
  expect(pdf.conteudo.subarray(0, 5).toString()).toBe('%PDF-');
  expect(pdf.conteudo.toString('latin1')).not.toMatch(
    /access_token|codigo_ativacao|senha_hash/i,
  );
  expect(pdf.resposta.url()).not.toContain(tokenInstrutor);
});

async function tokenDaSessao(page: Page): Promise<string> {
  const token = await page.evaluate(() =>
    sessionStorage.getItem('access_token'),
  );
  expect(token).toBeTruthy();
  return token!;
}

async function baixarConsolidado(page: Page, formato: 'CSV' | 'PDF') {
  const extensao = formato.toLowerCase();
  const respostaPromise = page.waitForResponse((resposta) =>
    resposta.url().includes(`/passagens/ciclos/exportacoes.${extensao}`),
  );
  const downloadPromise = page.waitForEvent('download');
  await page.getByRole('button', { name: `Exportar ${formato}` }).click();
  const [resposta, download] = await Promise.all([
    respostaPromise,
    downloadPromise,
  ]);
  expect(resposta.status()).toBe(200);
  return { resposta, download, conteudo: await lerDownload(download) };
}

async function lerDownload(download: Download): Promise<Buffer> {
  const stream = await download.createReadStream();
  const partes: Buffer[] = [];
  for await (const parte of stream) {
    partes.push(Buffer.isBuffer(parte) ? parte : Buffer.from(parte));
  }
  return Buffer.concat(partes);
}
