import { useAuth } from '@/features/auth/useAuth';

export function ShellPage() {
  const { logout } = useAuth();

  return (
    <main className="shell">
      <section className="shell__card" aria-labelledby="shell-title">
        <span className="shell__eyebrow">Ambiente de modernização</span>
        <h1 id="shell-title">RailOps</h1>
        <p>
          O novo frontend está preparado. Os fluxos operacionais continuam
          disponíveis no frontend legado durante a migração incremental.
        </p>
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
