import { describe, expect, it, vi } from 'vitest';

import {
  ApiClient,
  ApiClientError,
  UNAUTHORIZED_EVENT,
} from '@/services/api/client';
import { tokenStorage } from '@/services/api/tokenStorage';

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

describe('ApiClient', () => {
  it('centraliza a URL, o JSON e o token bearer', async () => {
    tokenStorage.set('jwt-seguro');
    const fetcher = vi
      .fn<typeof fetch>()
      .mockResolvedValue(jsonResponse({ ok: true }));
    const client = new ApiClient({ baseUrl: 'https://api.exemplo/', fetcher });

    await expect(
      client.request<{ ok: boolean }>('/recurso', {
        method: 'POST',
        body: JSON.stringify({ valor: 1 }),
      }),
    ).resolves.toEqual({ ok: true });

    const [url, init] = fetcher.mock.calls[0];
    const headers = new Headers(init?.headers);
    expect(url).toBe('https://api.exemplo/recurso');
    expect(headers.get('Authorization')).toBe('Bearer jwt-seguro');
    expect(headers.get('Content-Type')).toBe('application/json');
  });

  it('normaliza o envelope de erro da API', async () => {
    const fetcher = vi.fn<typeof fetch>().mockResolvedValue(
      jsonResponse(
        {
          detail: 'Credenciais inválidas.',
          error: {
            code: 'INVALID_CREDENTIALS',
            message: 'Credenciais inválidas.',
            details: null,
          },
        },
        401,
      ),
    );
    const client = new ApiClient({ fetcher });

    await expect(client.request('/auth/login')).rejects.toMatchObject({
      status: 401,
      code: 'INVALID_CREDENTIALS',
      message: 'Credenciais inválidas.',
    } satisfies Partial<ApiClientError>);
  });

  it('remove a sessão e sinaliza respostas 401', async () => {
    tokenStorage.set('jwt-expirado');
    const listener = vi.fn();
    window.addEventListener(UNAUTHORIZED_EVENT, listener, { once: true });
    const fetcher = vi
      .fn<typeof fetch>()
      .mockResolvedValue(jsonResponse({ detail: 'Não autenticado.' }, 401));

    await expect(
      new ApiClient({ fetcher }).request('/protegido'),
    ).rejects.toBeInstanceOf(ApiClientError);

    expect(tokenStorage.get()).toBeNull();
    expect(listener).toHaveBeenCalledOnce();
  });

  it('preserva a sessão válida quando o perfil recebe 403', async () => {
    tokenStorage.set('jwt-valido');
    const listener = vi.fn();
    window.addEventListener(UNAUTHORIZED_EVENT, listener, { once: true });
    const fetcher = vi
      .fn<typeof fetch>()
      .mockResolvedValue(jsonResponse({ detail: 'Sem permissão.' }, 403));

    await expect(
      new ApiClient({ fetcher }).request('/restrito'),
    ).rejects.toBeInstanceOf(ApiClientError);

    expect(tokenStorage.get()).toBe('jwt-valido');
    expect(listener).not.toHaveBeenCalled();
  });

  it('baixa arquivo autenticado e usa o nome do cabeçalho', async () => {
    tokenStorage.set('jwt-download');
    const fetcher = vi.fn<typeof fetch>().mockResolvedValue(
      new Response('arquivo', {
        headers: {
          'Content-Type': 'application/pdf',
          'Content-Disposition': 'attachment; filename="relatorio.pdf"',
        },
      }),
    );

    const arquivo = await new ApiClient({
      baseUrl: 'https://api.exemplo',
      fetcher,
    }).download('/relatorio');

    expect(arquivo.filename).toBe('relatorio.pdf');
    expect(arquivo.blob.size).toBeGreaterThan(0);
    const [url, init] = fetcher.mock.calls[0];
    expect(url).toBe('https://api.exemplo/relatorio');
    expect(String(url)).not.toContain('jwt-download');
    expect(new Headers(init?.headers).get('Authorization')).toBe(
      'Bearer jwt-download',
    );
  });

  it('preserva a sessão quando download consolidado recebe 403', async () => {
    tokenStorage.set('jwt-valido');
    const fetcher = vi.fn<typeof fetch>().mockResolvedValue(
      jsonResponse(
        {
          error: {
            code: 'SPECIAL_ACCESS_DENIED',
            message: 'Usuário sem permissão.',
            details: null,
          },
        },
        403,
      ),
    );

    await expect(
      new ApiClient({ fetcher }).download('/exportacoes.csv'),
    ).rejects.toMatchObject({ status: 403 });
    expect(tokenStorage.get()).toBe('jwt-valido');
  });
});
