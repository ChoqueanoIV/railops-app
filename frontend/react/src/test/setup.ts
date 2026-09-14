import '@testing-library/jest-dom/vitest';

import { cleanup } from '@testing-library/react';
import { afterEach, beforeEach, vi } from 'vitest';
import { authService } from '@/features/auth/service';

beforeEach(() => {
  vi.spyOn(authService, 'me').mockResolvedValue({
    nome: 'Operador de Teste',
    matricula: '30032552',
    perfil: 'MANOBRADOR',
  });
});

afterEach(() => {
  cleanup();
  sessionStorage.clear();
  vi.restoreAllMocks();
});
