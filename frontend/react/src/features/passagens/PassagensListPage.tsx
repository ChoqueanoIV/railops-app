import { FormEvent, useCallback, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import { ApiClientError } from '@/services/api/client';
import { passagemService } from './service';
import type {
  CicloConsultaFiltros,
  CicloConsultaLista,
  Turma,
  Turno,
} from './types';

const formatarDataLocal = (data: Date) => {
  const ano = data.getFullYear();
  const mes = String(data.getMonth() + 1).padStart(2, '0');
  const dia = String(data.getDate()).padStart(2, '0');
  return `${ano}-${mes}-${dia}`;
};

const periodoPadrao = () => {
  const fim = new Date();
  const inicio = new Date(fim);
  inicio.setDate(inicio.getDate() - 29);
  return {
    data_inicio: formatarDataLocal(inicio),
    data_fim: formatarDataLocal(fim),
  };
};

const filtrosIniciais = (): CicloConsultaFiltros => ({
  ...periodoPadrao(),
  pagina: 1,
  por_pagina: 20,
});

export function PassagensListPage() {
  const [formulario, setFormulario] =
    useState<CicloConsultaFiltros>(filtrosIniciais);
  const [filtros, setFiltros] = useState<CicloConsultaFiltros>(formulario);
  const [resultado, setResultado] = useState<CicloConsultaLista | null>(null);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState('');

  const consultar = useCallback(async () => {
    setCarregando(true);
    setErro('');
    try {
      setResultado(await passagemService.listar(filtros));
    } catch (error) {
      setErro(
        error instanceof ApiClientError
          ? error.message
          : 'Não foi possível consultar as passagens.',
      );
    } finally {
      setCarregando(false);
    }
  }, [filtros]);

  useEffect(() => {
    void consultar();
  }, [consultar]);

  const alterar = (campo: keyof CicloConsultaFiltros, valor: string) => {
    setFormulario((atual) => ({ ...atual, [campo]: valor || undefined }));
  };

  const aplicarFiltros = (evento: FormEvent) => {
    evento.preventDefault();
    setFiltros({ ...formulario, pagina: 1, por_pagina: 20 });
  };

  const limparFiltros = () => {
    const novos = filtrosIniciais();
    setFormulario(novos);
    setFiltros(novos);
  };

  const mudarPagina = (pagina: number) => {
    setFiltros((atual) => ({ ...atual, pagina }));
  };

  return (
    <main className="operation-page passage-list-page">
      <header className="operation-header">
        <Link to="/terminal">← Início</Link>
        <div>
          <span className="shell__eyebrow">Histórico operacional</span>
          <h1>Consultar passagens</h1>
          <p className="muted">
            Cada resultado reúne Brisamar e TECON em uma passagem completa.
          </p>
        </div>
      </header>

      <form className="filter-panel" onSubmit={aplicarFiltros}>
        <div className="form-grid">
          <label className="field">
            Data inicial
            <input
              type="date"
              value={formulario.data_inicio ?? ''}
              onChange={(e) => alterar('data_inicio', e.target.value)}
            />
          </label>
          <label className="field">
            Data final
            <input
              type="date"
              value={formulario.data_fim ?? ''}
              onChange={(e) => alterar('data_fim', e.target.value)}
            />
          </label>
          <label className="field">
            Turma
            <select
              value={formulario.turma ?? ''}
              onChange={(e) => alterar('turma', e.target.value as Turma)}
            >
              <option value="">Todas</option>
              {(['A', 'B', 'C', 'D'] as Turma[]).map((turma) => (
                <option key={turma}>{turma}</option>
              ))}
            </select>
          </label>
          <label className="field">
            Turno
            <select
              value={formulario.turno ?? ''}
              onChange={(e) => alterar('turno', e.target.value as Turno)}
            >
              <option value="">Todos</option>
              <option value="DIURNO">Diurno</option>
              <option value="NOTURNO">Noturno</option>
            </select>
          </label>
          <label className="field">
            Responsável
            <input
              value={formulario.responsavel ?? ''}
              placeholder="Nome ou matrícula"
              onChange={(e) => alterar('responsavel', e.target.value)}
            />
          </label>
          <label className="field">
            Protocolo
            <input
              value={formulario.protocolo ?? ''}
              placeholder="UUID da passagem"
              onChange={(e) => alterar('protocolo', e.target.value)}
            />
          </label>
        </div>
        <div className="filter-actions">
          <button className="button" type="submit">
            Aplicar filtros
          </button>
          <button
            className="button button--secondary"
            type="button"
            onClick={limparFiltros}
          >
            Limpar filtros
          </button>
        </div>
      </form>

      <section className="passage-results" aria-live="polite">
        {carregando && <p className="status">Carregando passagens...</p>}
        {!carregando && erro && (
          <div className="status status--error" role="alert">
            <p>{erro}</p>
            <button className="button button--secondary" onClick={consultar}>
              Tentar novamente
            </button>
          </div>
        )}
        {!carregando && !erro && resultado?.itens.length === 0 && (
          <p className="status">Nenhuma passagem encontrada neste período.</p>
        )}
        {!carregando && !erro && resultado && resultado.itens.length > 0 && (
          <>
            <p className="result-count">
              {resultado.paginacao.total_itens} passagem(ns) encontrada(s)
            </p>
            <div className="passage-list">
              {resultado.itens.map((ciclo) => (
                <article className="passage-card" key={ciclo.id}>
                  <div>
                    <span className="shell__eyebrow">
                      {ciclo.data} · Turma {ciclo.turma} ·{' '}
                      {ciclo.turno === 'DIURNO' ? 'Diurno' : 'Noturno'}
                    </span>
                    <h2>{ciclo.responsavel.nome}</h2>
                    <p className="muted">
                      Matrícula {ciclo.responsavel.matricula}
                    </p>
                    <p className="muted passage-protocol">{ciclo.id}</p>
                    <p>
                      Confirmada em{' '}
                      {ciclo.confirmado_em
                        ? new Intl.DateTimeFormat('pt-BR', {
                            dateStyle: 'short',
                            timeStyle: 'short',
                          }).format(new Date(ciclo.confirmado_em))
                        : '—'}
                    </p>
                  </div>
                  <Link
                    className="button button--secondary link-button"
                    to={`/confirmacao?ciclo=${ciclo.id}`}
                  >
                    Ver passagem completa
                  </Link>
                  {ciclo.passagens.map((passagem) => (
                    <Link
                      key={passagem.id}
                      className="text-link"
                      to={`/passagens/${passagem.id}/historico`}
                    >
                      Histórico{' '}
                      {passagem.terminal === 'BRISAMAR' ? 'Brisamar' : 'TECON'}
                    </Link>
                  ))}
                </article>
              ))}
            </div>
            <nav className="pagination" aria-label="Paginação">
              <button
                className="button button--secondary"
                disabled={resultado.paginacao.pagina <= 1}
                onClick={() => mudarPagina(resultado.paginacao.pagina - 1)}
              >
                Anterior
              </button>
              <span>
                Página {resultado.paginacao.pagina} de{' '}
                {resultado.paginacao.total_paginas}
              </span>
              <button
                className="button button--secondary"
                disabled={
                  resultado.paginacao.pagina >=
                  resultado.paginacao.total_paginas
                }
                onClick={() => mudarPagina(resultado.paginacao.pagina + 1)}
              >
                Próxima
              </button>
            </nav>
          </>
        )}
      </section>
    </main>
  );
}
