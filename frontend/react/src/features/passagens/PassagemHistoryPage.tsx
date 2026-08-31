import { useCallback, useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';

import { ApiClientError } from '@/services/api/client';
import { passagemService } from './service';
import type { PassagemConsulta, PassagemHistoricoLista } from './types';

type ValorPlano = string | number | boolean | null;

function achatar(valor: unknown, prefixo = ''): Record<string, ValorPlano> {
  if (valor === null || typeof valor !== 'object') {
    return prefixo ? { [prefixo]: valor as ValorPlano } : {};
  }
  return Object.entries(valor).reduce<Record<string, ValorPlano>>(
    (resultado, [chave, item]) => ({
      ...resultado,
      ...achatar(item, prefixo ? `${prefixo}.${chave}` : chave),
    }),
    {},
  );
}

function snapshotAtual(passagem: PassagemConsulta): Record<string, unknown> {
  return {
    passagem: {
      observacoes: passagem.observacoes,
      relatorio_ocorrencias: passagem.relatorio_ocorrencias,
      mobile_utilizado: passagem.mobile_utilizado,
      mobile_justificativa: passagem.mobile_justificativa,
    },
    detalhe: passagem.detalhe,
    equipe: passagem.equipe,
    ocupacoes_linhas: passagem.ocupacoes_linhas,
    radios_utilizados: passagem.radios_utilizados,
  };
}

function formatarValor(valor: ValorPlano | undefined) {
  if (valor === undefined || valor === null || valor === '')
    return 'Não informado';
  if (typeof valor === 'boolean') return valor ? 'Sim' : 'Não';
  return String(valor);
}

export function PassagemHistoryPage() {
  const { passagemId = '' } = useParams();
  const [pagina, setPagina] = useState(1);
  const [resultado, setResultado] = useState<PassagemHistoricoLista | null>(
    null,
  );
  const [erro, setErro] = useState('');
  const [carregando, setCarregando] = useState(true);

  const carregar = useCallback(async () => {
    setCarregando(true);
    setErro('');
    try {
      setResultado(
        await passagemService.consultarHistorico(passagemId, pagina),
      );
    } catch (e) {
      setErro(
        e instanceof ApiClientError && e.status === 403
          ? 'Seu perfil não possui permissão para consultar o histórico de edições.'
          : e instanceof Error
            ? e.message
            : 'Não foi possível carregar o histórico.',
      );
    } finally {
      setCarregando(false);
    }
  }, [pagina, passagemId]);

  useEffect(() => void carregar(), [carregar]);

  return (
    <main className="operation-page history-page">
      <header className="operation-header">
        <Link to="/passagens">← Passagens</Link>
        <div>
          <span className="shell__eyebrow">Auditoria operacional</span>
          <h1>Histórico de edições</h1>
          <p className="muted passage-protocol">Passagem {passagemId}</p>
        </div>
      </header>

      {carregando && <p className="status">Carregando histórico...</p>}
      {!carregando && erro && (
        <div className="status status--error" role="alert">
          <p>{erro}</p>
          <button className="button button--secondary" onClick={carregar}>
            Tentar novamente
          </button>
        </div>
      )}
      {!carregando && resultado && (
        <Historico
          resultado={resultado}
          pagina={pagina}
          mudarPagina={setPagina}
        />
      )}
    </main>
  );
}

function Historico({
  resultado,
  pagina,
  mudarPagina,
}: {
  resultado: PassagemHistoricoLista;
  pagina: number;
  mudarPagina: (pagina: number) => void;
}) {
  const atual = snapshotAtual(resultado.passagem_atual);
  return (
    <section className="history-content">
      <div className="history-summary">
        <strong>{resultado.passagem_atual.terminal}</strong>
        <span>{resultado.paginacao.total_itens} edição(ões) registrada(s)</span>
      </div>
      {resultado.itens.length === 0 && (
        <p className="status">Esta passagem ainda não possui edições.</p>
      )}
      <div className="history-list">
        {resultado.itens.map((item) => {
          const destino = atual;
          const anterior = achatar(item.snapshot);
          const posterior = achatar(destino);
          const campos = [
            ...new Set([...Object.keys(anterior), ...Object.keys(posterior)]),
          ].filter((campo) => anterior[campo] !== posterior[campo]);
          return (
            <article className="history-card" key={item.versao}>
              <header>
                <h2>Versão {item.versao}</h2>
                <p>
                  {new Intl.DateTimeFormat('pt-BR', {
                    dateStyle: 'short',
                    timeStyle: 'short',
                  }).format(new Date(item.alterado_em))}
                </p>
                <p>
                  {item.alterador.nome} · {item.alterador.matricula}
                </p>
              </header>
              {campos.length === 0 ? (
                <p className="muted">
                  Nenhuma diferença de conteúdo identificada.
                </p>
              ) : (
                <dl className="history-diff">
                  {campos.map((campo) => (
                    <div key={campo}>
                      <dt>{campo.replaceAll('_', ' ')}</dt>
                      <dd>
                        <span>Antes</span>
                        {formatarValor(anterior[campo])}
                      </dd>
                      <dd>
                        <span>Depois</span>
                        {formatarValor(posterior[campo])}
                      </dd>
                    </div>
                  ))}
                </dl>
              )}
            </article>
          );
        })}
      </div>
      {resultado.paginacao.total_paginas > 1 && (
        <nav className="pagination" aria-label="Paginação do histórico">
          <button
            className="button button--secondary"
            disabled={pagina <= 1}
            onClick={() => mudarPagina(pagina - 1)}
          >
            Anterior
          </button>
          <span>
            Página {pagina} de {resultado.paginacao.total_paginas}
          </span>
          <button
            className="button button--secondary"
            disabled={pagina >= resultado.paginacao.total_paginas}
            onClick={() => mudarPagina(pagina + 1)}
          >
            Próxima
          </button>
        </nav>
      )}
    </section>
  );
}
