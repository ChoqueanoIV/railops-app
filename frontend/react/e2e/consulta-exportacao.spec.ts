import {
  expect,
  test,
  type APIRequestContext,
  type Page,
} from '@playwright/test';

const API_URL = 'http://127.0.0.1:18000';
const MATRICULA = '91000003';
const PIN = '1234';
const TURMA = 'D';

test('localiza o ciclo confirmado e baixa o PDF individual autenticado', async ({
  page,
  request,
}) => {
  const data = dataOperacionalAtual();
  const cicloId = await prepararCicloConfirmado(request, data);
  await autenticar(page);

  await page.getByRole('link', { name: 'Consultar passagens' }).click();
  await expect(
    page.getByRole('heading', { name: 'Consultar passagens' }),
  ).toBeVisible();
  await page.getByLabel('Data inicial').fill(data);
  await page.getByLabel('Data final').fill(data);
  await page.getByLabel('Turma').selectOption(TURMA);
  await page.getByLabel('Responsável').fill(MATRICULA);
  await page.getByRole('button', { name: 'Aplicar filtros' }).click();

  const resultado = page.locator('article').filter({ hasText: cicloId });
  await expect(resultado).toContainText('Instrutor E2E');
  await expect(resultado).toContainText(`Matrícula ${MATRICULA}`);
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

async function autenticar(page: Page) {
  await page.goto('/login');
  await page.getByLabel('Matrícula').fill(MATRICULA);
  await page.getByLabel('PIN', { exact: true }).fill(PIN);
  await page.getByRole('button', { name: 'Entrar' }).click();
  await expect(
    page.getByRole('heading', { name: 'Selecione o terminal' }),
  ).toBeVisible();
}

async function prepararCicloConfirmado(
  request: APIRequestContext,
  data: string,
): Promise<string> {
  const login = await request.post(`${API_URL}/auth/login`, {
    data: { matricula: MATRICULA, pin: PIN },
  });
  expect(login.ok()).toBe(true);
  const { access_token: token } = (await login.json()) as {
    access_token: string;
  };
  const headers = { Authorization: `Bearer ${token}` };

  const brisamar = await request.post(`${API_URL}/passagens/brisamar`, {
    headers,
    data: payloadBrisamar(data),
  });
  expect(brisamar.status()).toBe(201);
  const { ciclo_id: cicloId } = (await brisamar.json()) as {
    ciclo_id: string;
  };

  const tecon = await request.post(`${API_URL}/passagens/tecon`, {
    headers,
    data: payloadTecon(data),
  });
  expect(tecon.status()).toBe(201);

  const confirmacao = await request.post(
    `${API_URL}/passagens/ciclos/${cicloId}/confirmar`,
    { headers },
  );
  expect(confirmacao.ok()).toBe(true);
  return cicloId;
}

function basePayload(data: string, linhas: string[]) {
  return {
    data,
    turma: TURMA,
    turno: turnoAtual(),
    observacoes: 'Ciclo preparado para consulta E2E',
    relatorio_ocorrencias: 'Sem ocorrências',
    mobile_utilizado: true,
    mobile_justificativa: null,
    equipe: [{ nome: 'Instrutor E2E', matricula: MATRICULA }],
    ocupacoes_linhas: linhas.map((codigo_linha) => ({
      codigo_linha,
      veiculos: null,
      sup_inf: null,
    })),
    radios_utilizados: [],
  };
}

function payloadBrisamar(data: string) {
  return {
    ...basePayload(data, [
      '16',
      '18',
      '20',
      '22 SUP',
      '22 INF',
      'Travessão L22',
      '24 SUP',
      '24 INF',
      'Travessão L24',
      '26',
      '28',
      '30',
    ]),
    detalhe: {
      radios_operantes: 2,
      radios_inoperantes: 0,
      baterias: 2,
      carregadores: 1,
      eots_disponiveis: null,
      eots_avariados: null,
    },
  };
}

function payloadTecon(data: string) {
  return {
    ...basePayload(data, [
      'Viaduto/DM1A',
      'L1',
      'L2',
      'Travessão',
      'DM4',
      'DM6',
      'DM1',
      'DM3',
      'Funil/DM2',
    ]),
    detalhe: { houve_atendimento: false },
  };
}

function agoraEmSaoPaulo() {
  const partes = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'America/Sao_Paulo',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    hourCycle: 'h23',
  }).formatToParts(new Date());
  const valor = (tipo: Intl.DateTimeFormatPartTypes) =>
    partes.find((parte) => parte.type === tipo)?.value ?? '';
  return {
    data: `${valor('year')}-${valor('month')}-${valor('day')}`,
    hora: Number(valor('hour')),
  };
}

function turnoAtual(): 'DIURNO' | 'NOTURNO' {
  const { hora } = agoraEmSaoPaulo();
  return hora >= 7 && hora < 19 ? 'DIURNO' : 'NOTURNO';
}

function dataOperacionalAtual(): string {
  const { data, hora } = agoraEmSaoPaulo();
  if (hora >= 7) return data;
  const anterior = new Date(`${data}T12:00:00-03:00`);
  anterior.setDate(anterior.getDate() - 1);
  return new Intl.DateTimeFormat('en-CA', {
    timeZone: 'America/Sao_Paulo',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(anterior);
}
