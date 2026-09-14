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
  UsuarioAtual,
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
  const [usuario, setUsuario] = useState<UsuarioAtual | null>(null);
  const [carregandoPerfil, setCarregandoPerfil] = useState(() =>
    Boolean(tokenStorage.get()),
  );

  useEffect(() => {
    if (!tokenStorage.get()) return;
    let ativo = true;
    service
      .me()
      .then((perfil) => {
        if (ativo) setUsuario(perfil);
      })
      .catch(() => {
        if (ativo) setUsuario(null);
      })
      .finally(() => {
        if (ativo) setCarregandoPerfil(false);
      });
    return () => {
      ativo = false;
    };
  }, [service]);

  const logout = useCallback(() => {
    tokenStorage.clear();
    setIsAuthenticated(false);
    setUsuario(null);
    setCarregandoPerfil(false);
  }, []);

  useEffect(() => {
    window.addEventListener(UNAUTHORIZED_EVENT, logout);
    return () => window.removeEventListener(UNAUTHORIZED_EVENT, logout);
  }, [logout]);

  const login = useCallback(
    async (payload: LoginRequest) => {
      const response = await service.login(payload);
      tokenStorage.set(response.access_token);
      setCarregandoPerfil(true);
      setIsAuthenticated(true);
      try {
        setUsuario(await service.me());
      } catch (erro) {
        logout();
        throw erro;
      } finally {
        setCarregandoPerfil(false);
      }
    },
    [service, logout],
  );

  const primeiroAcesso = useCallback(
    async (payload: PrimeiroAcessoRequest) => {
      const response = await service.primeiroAcesso(payload);
      return response.mensagem;
    },
    [service],
  );

  const value = useMemo<AuthContextValue>(
    () => ({
      isAuthenticated,
      usuario,
      carregandoPerfil,
      login,
      logout,
      primeiroAcesso,
    }),
    [isAuthenticated, usuario, carregandoPerfil, login, logout, primeiroAcesso],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
