import { useState, type FormEvent } from 'react';
import { Navigate, useLocation, useNavigate } from 'react-router-dom';

import { useAuth } from '@/features/auth/useAuth';
import { ApiClientError } from '@/services/api/client';

type AuthMode = 'login' | 'primeiro-acesso';

interface LocationState {
  from?: string;
}

function errorMessage(error: unknown, fallback: string): string {
  return error instanceof ApiClientError ? error.message : fallback;
}

export function LoginPage() {
  const { isAuthenticated, login, primeiroAcesso } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [mode, setMode] = useState<AuthMode>('login');
  const [matricula, setMatricula] = useState('');
  const [pin, setPin] = useState('');
  const [codigoAtivacao, setCodigoAtivacao] = useState('');
  const [confirmacaoPin, setConfirmacaoPin] = useState('');
  const [message, setMessage] = useState('');
  const [messageKind, setMessageKind] = useState<'error' | 'success'>('error');
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (isAuthenticated) {
    return <Navigate to="/terminal" replace />;
  }

  const toggleMode = () => {
    setMode((current) => (current === 'login' ? 'primeiro-acesso' : 'login'));
    setPin('');
    setCodigoAtivacao('');
    setConfirmacaoPin('');
    setMessage('');
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setMessage('');

    if (mode === 'primeiro-acesso' && pin !== confirmacaoPin) {
      setMessageKind('error');
      setMessage('O PIN e a confirmação não coincidem.');
      return;
    }

    setIsSubmitting(true);

    try {
      if (mode === 'primeiro-acesso') {
        await primeiroAcesso({
          matricula,
          codigo_ativacao: codigoAtivacao,
          pin,
        });
        setMode('login');
        setPin('');
        setCodigoAtivacao('');
        setConfirmacaoPin('');
        setMessageKind('success');
        setMessage('PIN definido com sucesso. Agora você pode entrar.');
        return;
      }

      await login({ matricula, pin });
      const destination =
        (location.state as LocationState | null)?.from ?? '/terminal';
      navigate(destination, { replace: true });
    } catch (error) {
      setMessageKind('error');
      setMessage(
        errorMessage(
          error,
          mode === 'login'
            ? 'Não foi possível realizar o login.'
            : 'Não foi possível definir o PIN.',
        ),
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  const firstAccess = mode === 'primeiro-acesso';

  return (
    <main className="auth-page">
      <section className="auth-card" aria-labelledby="auth-title">
        <span className="shell__eyebrow">Passagem de Serviço Ferroviária</span>
        <h1 id="auth-title">
          {firstAccess ? 'Definir primeiro PIN' : 'Acessar o RailOps'}
        </h1>
        <p className="auth-card__intro">
          {firstAccess
            ? 'Use os dados de ativação recebidos para cadastrar seu PIN.'
            : 'Entre com sua matrícula e seu PIN de quatro dígitos.'}
        </p>

        <form className="auth-form" onSubmit={handleSubmit}>
          <label>
            Matrícula
            <input
              name="matricula"
              value={matricula}
              onChange={(event) => setMatricula(event.target.value)}
              autoComplete="username"
              inputMode="numeric"
              pattern="[0-9]{8}"
              minLength={8}
              maxLength={8}
              required
            />
          </label>

          {firstAccess && (
            <label>
              Código de ativação
              <input
                name="codigo_ativacao"
                type="password"
                value={codigoAtivacao}
                onChange={(event) => setCodigoAtivacao(event.target.value)}
                autoComplete="one-time-code"
                inputMode="numeric"
                pattern="[0-9]{6}"
                minLength={6}
                maxLength={6}
                required
              />
            </label>
          )}

          <label>
            {firstAccess ? 'Novo PIN' : 'PIN'}
            <input
              name="pin"
              type="password"
              value={pin}
              onChange={(event) => setPin(event.target.value)}
              autoComplete={firstAccess ? 'new-password' : 'current-password'}
              inputMode="numeric"
              pattern="[0-9]{4}"
              minLength={4}
              maxLength={4}
              required
            />
          </label>

          {firstAccess && (
            <label>
              Confirmar novo PIN
              <input
                name="confirmacao_pin"
                type="password"
                value={confirmacaoPin}
                onChange={(event) => setConfirmacaoPin(event.target.value)}
                autoComplete="new-password"
                inputMode="numeric"
                pattern="[0-9]{4}"
                minLength={4}
                maxLength={4}
                required
              />
            </label>
          )}

          <button className="button" type="submit" disabled={isSubmitting}>
            {isSubmitting
              ? 'Aguarde...'
              : firstAccess
                ? 'Definir meu PIN'
                : 'Entrar'}
          </button>
        </form>

        {message && (
          <p
            className={`auth-message auth-message--${messageKind}`}
            role="alert"
          >
            {message}
          </p>
        )}

        <button className="auth-mode-toggle" type="button" onClick={toggleMode}>
          {firstAccess
            ? 'Voltar para o login'
            : 'Primeiro acesso? Definir meu PIN'}
        </button>
      </section>
    </main>
  );
}
