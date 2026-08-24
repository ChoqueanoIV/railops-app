import {
  useCallback,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react';

import {
  AuthContext,
  type AuthContextValue,
} from '@/features/auth/AuthContext';
import { authService, type AuthService } from '@/features/auth/service';
import type {
  LoginRequest,
  PrimeiroAcessoRequest,
} from '@/features/auth/types';
import { UNAUTHORIZED_EVENT } from '@/services/api/client';
import { tokenStorage } from '@/services/api/tokenStorage';

interface AuthProviderProps {
  children: ReactNode;
  service?: AuthService;
}

export function AuthProvider({
  children,
  service = authService,
}: AuthProviderProps) {
  const [isAuthenticated, setIsAuthenticated] = useState(() =>
    Boolean(tokenStorage.get()),
  );

  const logout = useCallback(() => {
    tokenStorage.clear();
    setIsAuthenticated(false);
  }, []);

  useEffect(() => {
    window.addEventListener(UNAUTHORIZED_EVENT, logout);
    return () => window.removeEventListener(UNAUTHORIZED_EVENT, logout);
  }, [logout]);

  const login = useCallback(
    async (payload: LoginRequest) => {
      const response = await service.login(payload);
      tokenStorage.set(response.access_token);
      setIsAuthenticated(true);
    },
    [service],
  );

  const primeiroAcesso = useCallback(
    async (payload: PrimeiroAcessoRequest) => {
      const response = await service.primeiroAcesso(payload);
      return response.mensagem;
    },
    [service],
  );

  const value = useMemo<AuthContextValue>(
    () => ({ isAuthenticated, login, logout, primeiroAcesso }),
    [isAuthenticated, login, logout, primeiroAcesso],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
