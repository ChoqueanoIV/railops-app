import type {
  LoginRequest,
  LoginResponse,
  PrimeiroAcessoRequest,
  PrimeiroAcessoResponse,
} from '@/features/auth/types';
import { apiClient, type ApiClient } from '@/services/api/client';

export class AuthService {
  constructor(private readonly client: ApiClient) {}

  login(payload: LoginRequest): Promise<LoginResponse> {
    return this.client.request<LoginResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  primeiroAcesso(
    payload: PrimeiroAcessoRequest,
  ): Promise<PrimeiroAcessoResponse> {
    return this.client.request<PrimeiroAcessoResponse>(
      '/auth/primeiro-acesso',
      {
        method: 'POST',
        body: JSON.stringify(payload),
      },
    );
  }
}

export const authService = new AuthService(apiClient);
