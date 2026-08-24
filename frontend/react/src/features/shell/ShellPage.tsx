import { Link } from 'react-router-dom';
import { useAuth } from '@/features/auth/useAuth';

export function ShellPage() {
  const { logout } = useAuth();

  return (
    <main className="shell">
      <section className="shell__card" aria-labelledby="shell-title">
        <span className="shell__eyebrow">Passagem de serviço</span>
        <h1 id="shell-title">Selecione o terminal</h1>
        <p>
          Registre as informações atualizadas do turno que está sendo encerrado.
        </p>
        <nav className="terminal-grid" aria-label="Terminais">
          <Link className="terminal-card" to="/brisamar">
            <strong>Pátio Brisamar</strong>
            <span>Linhas 16 a 30 e recursos entregues</span>
          </Link>
          <Link className="terminal-card" to="/tecon">
            <strong>Terminal TECON</strong>
            <span>Linhas e atendimento das Áreas 1 e 2</span>
          </Link>
        </nav>
        <button
          className="button button--secondary"
          type="button"
          onClick={logout}
        >
          Sair
        </button>
      </section>
    </main>
  );
}
