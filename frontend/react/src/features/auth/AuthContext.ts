import { createContext } from 'react';

import type {
  LoginRequest,
  PrimeiroAcessoRequest,
} from '@/features/auth/types';

export interface AuthContextValue {
  isAuthenticated: boolean;
  login(payload: LoginRequest): Promise<void>;
  logout(): void;
  primeiroAcesso(payload: PrimeiroAcessoRequest): Promise<string>;
}

export const AuthContext = createContext<AuthContextValue | null>(null);
