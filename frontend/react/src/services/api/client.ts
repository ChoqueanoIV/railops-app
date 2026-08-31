import { tokenStorage } from '@/services/api/tokenStorage';
import type { ApiErrorEnvelope } from '@/services/api/types';

const DEFAULT_TIMEOUT_MS = 10_000;
const DEFAULT_API_BASE_URL = 'http://127.0.0.1:8000';

export const UNAUTHORIZED_EVENT = 'railops:unauthorized';

export class ApiClientError extends Error {
  constructor(
    message: string,
    readonly status: number | null,
    readonly code: string,
    readonly details: unknown | null = null,
  ) {
    super(message);
    this.name = 'ApiClientError';
  }
}

interface ApiClientOptions {
  baseUrl?: string;
  fetcher?: typeof fetch;
  timeoutMs?: number;
}

export interface ApiDownload {
  blob: Blob;
  filename: string;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null;
}

function isApiErrorEnvelope(value: unknown): value is ApiErrorEnvelope {
  if (!isRecord(value) || !isRecord(value.error)) {
    return false;
  }

  return (
    typeof value.error.code === 'string' &&
    typeof value.error.message === 'string' &&
    'details' in value.error
  );
}

async function readBody(response: Response): Promise<unknown> {
  const contentType = response.headers.get('content-type') ?? '';

  if (!contentType.includes('application/json')) {
    return null;
  }

  try {
    return await response.json();
  } catch {
    return null;
  }
}

export class ApiClient {
  private readonly baseUrl: string;
  private readonly fetcher?: typeof fetch;
  private readonly timeoutMs: number;

  constructor(options: ApiClientOptions = {}) {
    this.baseUrl = (options.baseUrl ?? DEFAULT_API_BASE_URL).replace(/\/$/, '');
    this.fetcher = options.fetcher;
    this.timeoutMs = options.timeoutMs ?? DEFAULT_TIMEOUT_MS;
  }

  async request<T>(path: string, init: RequestInit = {}): Promise<T> {
    const controller = new AbortController();
    const timeoutId = window.setTimeout(
      () => controller.abort(),
      this.timeoutMs,
    );
    const headers = new Headers(init.headers);
    const token = tokenStorage.get();

    headers.set('Accept', 'application/json');
    if (init.body !== undefined && !headers.has('Content-Type')) {
      headers.set('Content-Type', 'application/json');
    }
    if (token) {
      headers.set('Authorization', `Bearer ${token}`);
    }

    try {
      const response = await (this.fetcher ?? fetch)(`${this.baseUrl}${path}`, {
        ...init,
        headers,
        signal: controller.signal,
      });
      const body = await readBody(response);

      if (!response.ok) {
        if (response.status === 401) {
          tokenStorage.clear();
          window.dispatchEvent(new Event(UNAUTHORIZED_EVENT));
        }

        if (isApiErrorEnvelope(body)) {
          throw new ApiClientError(
            body.error.message,
            response.status,
            body.error.code,
            body.error.details,
          );
        }

        throw new ApiClientError(
          'Não foi possível concluir a solicitação.',
          response.status,
          'HTTP_ERROR',
        );
      }

      return body as T;
    } catch (error) {
      if (error instanceof ApiClientError) {
        throw error;
      }
      if (error instanceof DOMException && error.name === 'AbortError') {
        throw new ApiClientError(
          'O servidor demorou para responder. Tente novamente.',
          null,
          'REQUEST_TIMEOUT',
        );
      }
      throw new ApiClientError(
        'Não foi possível conectar ao servidor.',
        null,
        'NETWORK_ERROR',
      );
    } finally {
      window.clearTimeout(timeoutId);
    }
  }

  async download(path: string): Promise<ApiDownload> {
    const controller = new AbortController();
    const timeoutId = window.setTimeout(
      () => controller.abort(),
      this.timeoutMs,
    );
    const headers = new Headers();
    const token = tokenStorage.get();
    if (token) headers.set('Authorization', `Bearer ${token}`);

    try {
      const response = await (this.fetcher ?? fetch)(`${this.baseUrl}${path}`, {
        headers,
        signal: controller.signal,
      });
      if (!response.ok) {
        const body = await readBody(response);
        if (response.status === 401) {
          tokenStorage.clear();
          window.dispatchEvent(new Event(UNAUTHORIZED_EVENT));
        }
        if (isApiErrorEnvelope(body)) {
          throw new ApiClientError(
            body.error.message,
            response.status,
            body.error.code,
            body.error.details,
          );
        }
        throw new ApiClientError(
          'Não foi possível concluir a solicitação.',
          response.status,
          'HTTP_ERROR',
        );
      }

      const disposicao = response.headers.get('content-disposition') ?? '';
      const nome = /filename="?([^";]+)"?/i.exec(disposicao)?.[1];
      return {
        blob: await response.blob(),
        filename: nome ?? 'railops-exportacao',
      };
    } catch (error) {
      if (error instanceof ApiClientError) throw error;
      if (error instanceof DOMException && error.name === 'AbortError') {
        throw new ApiClientError(
          'O servidor demorou para responder. Tente novamente.',
          null,
          'REQUEST_TIMEOUT',
        );
      }
      throw new ApiClientError(
        'Não foi possível conectar ao servidor.',
        null,
        'NETWORK_ERROR',
      );
    } finally {
      window.clearTimeout(timeoutId);
    }
  }
}

export const apiClient = new ApiClient({
  baseUrl: import.meta.env.VITE_API_BASE_URL ?? DEFAULT_API_BASE_URL,
});
