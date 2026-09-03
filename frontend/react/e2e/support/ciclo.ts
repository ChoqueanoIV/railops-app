import { expect, type APIRequestContext, type Page } from '@playwright/test';

const API_URL = 'http://127.0.0.1:18000';

export interface CredenciaisE2E {
  matricula: string;
  pin: string;
  turma: 'A' | 'B' | 'C' | 'D';
}

export const INSTRUTOR: CredenciaisE2E = {
  matricula: '91000003',
  pin: '1234',
  turma: 'D',
};

export const MANOBRADOR: CredenciaisE2E = {
  matricula: '91000002',
  pin: '1234',
  turma: 'C',
};

export async function autenticar(page: Page, usuario: CredenciaisE2E) {
  await page.goto('/login');
  await page.getByLabel('Matrícula').fill(usuario.matricula);
  await page.getByLabel('PIN', { exact: true }).fill(usuario.pin);
  await page.getByRole('button', { name: 'Entrar' }).click();
  await expect(
    page.getByRole('heading', { name: 'Selecione o terminal' }),
  ).toBeVisible();
}

export async function prepararCicloConfirmado(
  request: APIRequestContext,
  usuario: CredenciaisE2E = INSTRUTOR,
) {
  const data = dataOperacionalAtual();
  const login = await request.post(`${API_URL}/auth/login`, {
    data: { matricula: usuario.matricula, pin: usuario.pin },
  });
  expect(login.ok()).toBe(true);
  const { access_token: token } = (await login.json()) as {
    access_token: string;
  };
  const headers = { Authorization: `Bearer ${token}` };

  const brisamar = await request.post(`${API_URL}/passagens/brisamar`, {
    headers,
    data: payloadBrisamar(data, usuario),
  });
  expect(brisamar.status()).toBe(201);
  const resultadoBrisamar = (await brisamar.json()) as {
    id: string;
    ciclo_id: string;
  };

  const tecon = await request.post(`${API_URL}/passagens/tecon`, {
    headers,
    data: payloadTecon(data, usuario),
  });
  expect(tecon.status()).toBe(201);
  const resultadoTecon = (await tecon.json()) as { id: string };

  const confirmacao = await request.post(
    `${API_URL}/passagens/ciclos/${resultadoBrisamar.ciclo_id}/confirmar`,
    { headers },
  );
  expect(confirmacao.ok()).toBe(true);
  return {
    cicloId: resultadoBrisamar.ciclo_id,
    passagemBrisamarId: resultadoBrisamar.id,
    passagemTeconId: resultadoTecon.id,
    data,
  };
}

function basePayload(data: string, linhas: string[], usuario: CredenciaisE2E) {
  return {
    data,
    turma: usuario.turma,
    turno: turnoAtual(),
    observacoes: 'Ciclo preparado para consulta E2E',
    relatorio_ocorrencias: 'Sem ocorrências',
    mobile_utilizado: true,
    mobile_justificativa: null,
    equipe: [{ nome: 'Equipe E2E', matricula: usuario.matricula }],
    ocupacoes_linhas: linhas.map((codigo_linha) => ({
      codigo_linha,
      veiculos: null,
      sup_inf: null,
    })),
    radios_utilizados: [],
  };
}

function payloadBrisamar(data: string, usuario: CredenciaisE2E) {
  return {
    ...basePayload(
      data,
      [
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
      ],
      usuario,
    ),
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

function payloadTecon(data: string, usuario: CredenciaisE2E) {
  return {
    ...basePayload(
      data,
      [
        'Viaduto/DM1A',
        'L1',
        'L2',
        'Travessão',
        'DM4',
        'DM6',
        'DM1',
        'DM3',
        'Funil/DM2',
      ],
      usuario,
    ),
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
