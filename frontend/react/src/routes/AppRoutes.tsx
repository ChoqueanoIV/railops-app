import { Navigate, Route, Routes } from 'react-router-dom';

import { ShellPage } from '@/features/shell/ShellPage';

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<ShellPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
