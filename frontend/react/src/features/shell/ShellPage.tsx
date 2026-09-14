import { Link } from 'react-router-dom';
import { useAuth } from '@/features/auth/useAuth';
import { ProductBrand } from '@/components/ProductBrand';

export function ShellPage() {
  const { logout, usuario, carregandoPerfil } = useAuth();
  const podePreencher = usuario?.perfil === 'MANOBRADOR';

  return (
    <main className="shell">
      <section className="shell__card" aria-labelledby="shell-title">
        <ProductBrand />
        <span className="shell__eyebrow">
          {podePreencher ? 'Início do preenchimento' : 'Consulta de passagens'}
        </span>
        <h1 id="shell-title">
          {podePreencher ? 'Selecione o terminal' : 'Passagens registradas'}
        </h1>
        <p>
          {podePreencher
            ? 'Registre as informações atualizadas do turno que está sendo encerrado.'
            : 'Seu perfil permite consultar e auditar passagens, sem criar ou editar registros.'}
        </p>
        {carregandoPerfil && <p className="status">Verificando perfil...</p>}
        {podePreencher && (
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
        )}
        <Link className="button button--secondary link-button" to="/passagens">
          Consultar passagens
        </Link>
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
