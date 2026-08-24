import { useEffect, useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { passagemService } from './service';
import type { UltimaPassagem } from './types';

export function ConfirmationPage() {
  const [editavel, setEditavel] = useState(false);
  const [passagem] = useState<UltimaPassagem | null>(() => {
    const raw = sessionStorage.getItem('ultima_passagem');
    return raw ? JSON.parse(raw) : null;
  });
  useEffect(() => {
    if (!passagem) return;
    passagemService
      .consultar(passagem.id)
      .then((p) => setEditavel(p.editavel))
      .catch(() => setEditavel(false));
    sessionStorage.removeItem('ultima_passagem');
  }, [passagem]);
  if (!passagem) return <Navigate to="/terminal" replace />;
  const tecon = passagem.terminal === 'Terminal TECON';
  const destino = tecon ? '/tecon' : '/brisamar';
  return (
    <main className="shell">
      <section className="shell__card confirmation">
        <span className="shell__eyebrow">Registro concluído</span>
        <h1>
          {passagem.operacao === 'edicao'
            ? 'Passagem atualizada'
            : 'Passagem registrada'}
        </h1>
        <dl>
          <div>
            <dt>Terminal</dt>
            <dd>{passagem.terminal}</dd>
          </div>
          <div>
            <dt>Data do início</dt>
            <dd>
              {new Date(`${passagem.data}T00:00:00`).toLocaleDateString(
                'pt-BR',
              )}
            </dd>
          </div>
          <div>
            <dt>Turma / turno</dt>
            <dd>
              {passagem.turma} · {passagem.turno}
            </dd>
          </div>
          <div>
            <dt>Protocolo</dt>
            <dd>{passagem.id}</dd>
          </div>
        </dl>
        {editavel && (
          <Link
            className="button link-button"
            to={`${destino}?editar=${passagem.id}`}
          >
            Editar esta passagem
          </Link>
        )}
        <Link
          className="button button--secondary link-button"
          to={tecon ? '/brisamar' : '/tecon'}
        >
          Preencher o outro terminal
        </Link>
        <Link className="text-link" to="/terminal">
          Voltar aos terminais
        </Link>
      </section>
    </main>
  );
}
