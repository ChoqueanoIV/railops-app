import { Navigate, Route, Routes } from 'react-router-dom';

import { LoginPage } from '@/features/auth/LoginPage';
import { ProtectedRoute } from '@/features/auth/ProtectedRoute';
import { ShellPage } from '@/features/shell/ShellPage';

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route element={<ProtectedRoute />}>
        <Route path="/terminal" element={<ShellPage />} />
      </Route>
      <Route path="/" element={<Navigate to="/terminal" replace />} />
      <Route path="*" element={<Navigate to="/terminal" replace />} />
    </Routes>
  );
}
