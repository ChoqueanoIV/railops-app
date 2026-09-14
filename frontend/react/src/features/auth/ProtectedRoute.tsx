import { Navigate, Outlet, useLocation } from 'react-router-dom';

import { useAuth } from '@/features/auth/useAuth';

export function ProtectedRoute() {
  const { isAuthenticated } = useAuth();
  const location = useLocation();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  return <Outlet />;
}

export function ManobradorRoute() {
  const { usuario, carregandoPerfil } = useAuth();
  if (carregandoPerfil) return <p className="status">Verificando perfil...</p>;
  if (usuario?.perfil !== 'MANOBRADOR')
    return <Navigate to="/passagens" replace />;
  return <Outlet />;
}
