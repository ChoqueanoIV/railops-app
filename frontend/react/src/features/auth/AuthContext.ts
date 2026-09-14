import { createContext } from 'react';

import type {
  LoginRequest,
  PrimeiroAcessoRequest,
  UsuarioAtual,
} from '@/features/auth/types';

export interface AuthContextValue {
  isAuthenticated: boolean;
  usuario: UsuarioAtual | null;
  carregandoPerfil: boolean;
  login(payload: LoginRequest): Promise<void>;
  logout(): void;
  primeiroAcesso(payload: PrimeiroAcessoRequest): Promise<string>;
}

export const AuthContext = createContext<AuthContextValue | null>(null);
