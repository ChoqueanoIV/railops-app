import { Navigate, Route, Routes } from 'react-router-dom';

import { LoginPage } from '@/features/auth/LoginPage';
import { ProtectedRoute } from '@/features/auth/ProtectedRoute';
import { ShellPage } from '@/features/shell/ShellPage';
import { ConfirmationPage } from '@/features/passagens/ConfirmationPage';
import { PassagemPage } from '@/features/passagens/PassagemPage';
import { PassagensListPage } from '@/features/passagens/PassagensListPage';
import { PassagemHistoryPage } from '@/features/passagens/PassagemHistoryPage';

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route element={<ProtectedRoute />}>
        <Route path="/terminal" element={<ShellPage />} />
        <Route
          path="/brisamar"
          element={<PassagemPage terminal="BRISAMAR" />}
        />
        <Route path="/tecon" element={<PassagemPage terminal="TECON" />} />
        <Route path="/confirmacao" element={<ConfirmationPage />} />
        <Route path="/passagens" element={<PassagensListPage />} />
        <Route
          path="/passagens/:passagemId/historico"
          element={<PassagemHistoryPage />}
        />
      </Route>
      <Route path="/" element={<Navigate to="/terminal" replace />} />
      <Route path="*" element={<Navigate to="/terminal" replace />} />
    </Routes>
  );
}
