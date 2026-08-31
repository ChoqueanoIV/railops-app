import { useEffect, useState } from 'react';
import { Link, Navigate, useSearchParams } from 'react-router-dom';
import { passagemService, salvarDownload } from './service';
import type {
  CicloPassagem,
  PassagemConsulta,
  Terminal,
  UltimaPassagem,
} from './types';

const caminhoTerminal = (terminal: Terminal) =>
  terminal === 'BRISAMAR' ? '/brisamar' : '/tecon';
const nomeTerminal = (terminal: Terminal) =>
  terminal === 'BRISAMAR' ? 'Pátio Brisamar' : 'Terminal TECON';

export function ConfirmationPage() {
  const [params] = useSearchParams();
  const cicloId = params.get('ciclo');
  return cicloId ? <RevisaoCiclo cicloId={cicloId} /> : <ConfirmacaoLegada />;
}

function RevisaoCiclo({ cicloId }: { cicloId: string }) {
  const [ciclo, setCiclo] = useState<CicloPassagem | null>(null);
  const [erro, setErro] = useState('');
  const [confirmando, setConfirmando] = useState(false);
  const [baixandoPdf, setBaixandoPdf] = useState(false);

  useEffect(() => {
    passagemService
      .consultarCiclo(cicloId)
      .then(setCiclo)
      .catch((e: unknown) =>
        setErro(
          e instanceof Error
            ? e.message
            : 'Não foi possível carregar a revisão.',
        ),
      );
  }, [cicloId]);

  async function confirmar() {
    setConfirmando(true);
    setErro('');
    try {
      setCiclo(await passagemService.confirmarCiclo(cicloId));
    } catch (e) {
      setErro(e instanceof Error ? e.message : 'Não foi possível confirmar.');
    } finally {
      setConfirmando(false);
    }
  }

  async function baixarPdf() {
    setBaixandoPdf(true);
    setErro('');
    try {
      const arquivo = await passagemService.baixarPdfIndividual(cicloId);
      salvarDownload(arquivo.blob, arquivo.filename);
    } catch (e) {
      setErro(
        e instanceof Error ? e.message : 'Não foi possível baixar o PDF.',
      );
    } finally {
      setBaixandoPdf(false);
    }
  }

  if (erro && !ciclo) return <ErroRevisao mensagem={erro} />;
  if (!ciclo)
    return (
      <main className="shell">
        <p className="status">Carregando revisão completa...</p>
      </main>
    );

  const confirmado = ciclo.estado === 'CONFIRMADO';
  return (
    <main className="shell review-page">
      <section className="shell__card confirmation">
        <span className="shell__eyebrow">
          {confirmado ? 'Ciclo confirmado' : 'Revisão antes da confirmação'}
        </span>
        <h1>Passagem completa</h1>
        <dl>
          <div>
            <dt>Data do início</dt>
            <dd>
              {new Date(`${ciclo.data}T00:00:00`).toLocaleDateString('pt-BR')}
            </dd>
          </div>
          <div>
            <dt>Turma / turno</dt>
            <dd>
              {ciclo.turma} · {ciclo.turno}
            </dd>
          </div>
          <div>
            <dt>Protocolo do ciclo</dt>
            <dd>{ciclo.id}</dd>
          </div>
          <div>
            <dt>Estado</dt>
            <dd>{confirmado ? 'Confirmado — somente leitura' : 'Rascunho'}</dd>
          </div>
        </dl>
        {ciclo.terminal_pendente && (
          <Link
            className="button link-button"
            to={`${caminhoTerminal(ciclo.terminal_pendente)}?ciclo=${ciclo.id}`}
          >
            Preencher {nomeTerminal(ciclo.terminal_pendente)}
          </Link>
        )}
      </section>
      {ciclo.passagens.map((passagem) => (
        <DetalhePassagem
          key={passagem.id}
          passagem={passagem}
          cicloId={ciclo.id}
          confirmado={confirmado}
        />
      ))}
      <section className="shell__card confirmation review-actions">
        {erro && (
          <p role="alert" className="status status--error">
            {erro}
          </p>
        )}
        {!confirmado && !ciclo.terminal_pendente && (
          <button className="button" disabled={confirmando} onClick={confirmar}>
            {confirmando ? 'Confirmando...' : 'Confirmar passagem completa'}
          </button>
        )}
        {confirmado && (
          <>
            <p role="status">
              Confirmação final concluída. Brisamar e TECON estão bloqueados
              para edição.
            </p>
            <button
              className="button"
              disabled={baixandoPdf}
              onClick={baixarPdf}
            >
              {baixandoPdf ? 'Gerando PDF...' : 'Baixar PDF'}
            </button>
          </>
        )}
        <Link className="text-link" to="/terminal">
          Voltar aos terminais
        </Link>
      </section>
    </main>
  );
}

function DetalhePassagem({
  passagem,
  cicloId,
  confirmado,
}: {
  passagem: PassagemConsulta;
  cicloId: string;
  confirmado: boolean;
}) {
  return (
    <section className="shell__card review-terminal">
      <h2>{nomeTerminal(passagem.terminal)}</h2>
      <p>
        <strong>Observações:</strong>{' '}
        {passagem.observacoes || 'Sem observações'}
      </p>
      <p>
        <strong>Relatório de ocorrências:</strong>{' '}
        {passagem.relatorio_ocorrencias || 'Sem ocorrências'}
      </p>
      <h3>Equipe</h3>
      <ul>
        {passagem.equipe.map((membro) => (
          <li key={`${membro.matricula}-${membro.nome}`}>
            {membro.nome} — {membro.matricula}
          </li>
        ))}
      </ul>
      <h3>Ocupação das linhas</h3>
      <dl className="review-lines">
        {passagem.ocupacoes_linhas.map((linha) => (
          <div key={linha.codigo_linha}>
            <dt>{linha.codigo_linha}</dt>
            <dd>{linha.veiculos || 'Não informado'}</dd>
          </div>
        ))}
      </dl>
      <h3>Dados do terminal</h3>
      <dl className="review-lines">
        {Object.entries(passagem.detalhe).map(([campo, valor]) => (
          <div key={campo}>
            <dt>{campo.replaceAll('_', ' ')}</dt>
            <dd>{valor == null ? 'Não informado' : String(valor)}</dd>
          </div>
        ))}
      </dl>
      {!confirmado && passagem.editavel && (
        <Link
          className="button button--secondary link-button"
          to={`${caminhoTerminal(passagem.terminal)}?editar=${passagem.id}&ciclo=${cicloId}`}
        >
          Corrigir {nomeTerminal(passagem.terminal)}
        </Link>
      )}
    </section>
  );
}

function ErroRevisao({ mensagem }: { mensagem: string }) {
  return (
    <main className="shell">
      <section className="shell__card confirmation">
        <h1>Revisão indisponível</h1>
        <p role="alert" className="status status--error">
          {mensagem}
        </p>
        <Link className="text-link" to="/terminal">
          Voltar aos terminais
        </Link>
      </section>
    </main>
  );
}

function ConfirmacaoLegada() {
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
