import { FormEvent, useEffect, useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { ApiClientError } from '@/services/api/client';
import { passagemService } from './service';
import type {
  EquipeMembro,
  LinhaOcupacao,
  PassagemPayload,
  RadioUso,
  Terminal,
  Turma,
  Turno,
  UltimaPassagem,
} from './types';

const LINHAS: Record<Terminal, string[]> = {
  BRISAMAR: [
    '16',
    '18',
    '20',
    '22 SUP',
    '22 INF',
    'Travessão L22',
    '24 SUP',
    '24 INF',
    'Travessão L24',
    '26',
    '28',
    '30',
  ],
  TECON: [
    'Viaduto/DM1A',
    'L1',
    'L2',
    'Travessão',
    'DM4',
    'DM6',
    'DM1',
    'DM3',
    'Funil/DM2',
  ],
};
const vazio = (valor: string) => valor.trim() || null;
const novaEquipe = (): EquipeMembro => ({ nome: '', matricula: '' });
const novoRadio = (): RadioUso => ({
  numero: '',
  manobrador_nome: '',
  hora_retirada: null,
  hora_entrega: null,
  apresentou_falha: false,
  falha_descricao: null,
});
const novasLinhas = (terminal: Terminal): LinhaOcupacao[] =>
  LINHAS[terminal].map((codigo_linha) => ({
    codigo_linha,
    veiculos: null,
    sup_inf: null,
  }));

export function PassagemPage({ terminal }: { terminal: Terminal }) {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const id = params.get('editar') ?? undefined;
  const cicloId = params.get('ciclo') ?? undefined;
  const [carregando, setCarregando] = useState(Boolean(id || cicloId));
  const [enviando, setEnviando] = useState(false);
  const [erro, setErro] = useState('');
  const [data, setData] = useState('');
  const [turma, setTurma] = useState<Turma>('A');
  const [turno, setTurno] = useState<Turno>('DIURNO');
  const [observacoes, setObservacoes] = useState('');
  const [ocorrencias, setOcorrencias] = useState('');
  const [mobile, setMobile] = useState(true);
  const [justificativa, setJustificativa] = useState('');
  const [equipe, setEquipe] = useState<EquipeMembro[]>([novaEquipe()]);
  const [linhas, setLinhas] = useState<LinhaOcupacao[]>(novasLinhas(terminal));
  const [radios, setRadios] = useState<RadioUso[]>([]);
  const [recursos, setRecursos] = useState({
    radios_operantes: 0,
    radios_inoperantes: 0,
    baterias: 0,
    carregadores: 0,
    eots_disponiveis: '',
    eots_avariados: '',
  });
  const [houveAtendimento, setHouveAtendimento] = useState(false);
  const [cargaMalPosicionada, setCargaMalPosicionada] = useState(false);
  const [cargaDescricao, setCargaDescricao] = useState('');
  const [areas, setAreas] = useState({
    area1_atendida: false,
    area1_inicio: '',
    area1_termino: '',
    area2_atendida: false,
    area2_inicio: '',
    area2_termino: '',
  });

  useEffect(() => {
    if (!id) return;
    passagemService
      .consultar(id)
      .then((p) => {
        if (p.terminal !== terminal)
          throw new Error(`A passagem não pertence ao ${terminal}.`);
        if (!p.editavel)
          throw new Error('Esta passagem não pode mais ser editada.');
        setData(p.data);
        setTurma(p.turma);
        setTurno(p.turno);
        setObservacoes(p.observacoes ?? '');
        setOcorrencias(p.relatorio_ocorrencias ?? '');
        setMobile(p.mobile_utilizado);
        setJustificativa(p.mobile_justificativa ?? '');
        setEquipe(p.equipe.length ? p.equipe : [novaEquipe()]);
        setLinhas(p.ocupacoes_linhas);
        setRadios(p.radios_utilizados);
        if (terminal === 'BRISAMAR' && 'radios_operantes' in p.detalhe)
          setRecursos({
            ...p.detalhe,
            eots_disponiveis: p.detalhe.eots_disponiveis ?? '',
            eots_avariados: p.detalhe.eots_avariados ?? '',
          });
        if (terminal === 'TECON' && 'houve_atendimento' in p.detalhe) {
          setHouveAtendimento(p.detalhe.houve_atendimento);
          setCargaMalPosicionada(p.detalhe.carga_mal_posicionada ?? false);
          setCargaDescricao(p.detalhe.carga_mal_posicionada_descricao ?? '');
          setAreas({
            area1_atendida: p.detalhe.area1_atendida ?? false,
            area1_inicio: p.detalhe.area1_inicio?.slice(0, 5) ?? '',
            area1_termino: p.detalhe.area1_termino?.slice(0, 5) ?? '',
            area2_atendida: p.detalhe.area2_atendida ?? false,
            area2_inicio: p.detalhe.area2_inicio?.slice(0, 5) ?? '',
            area2_termino: p.detalhe.area2_termino?.slice(0, 5) ?? '',
          });
        }
      })
      .catch((e: unknown) =>
        setErro(
          e instanceof Error
            ? e.message
            : 'Não foi possível carregar a passagem.',
        ),
      )
      .finally(() => setCarregando(false));
  }, [id, terminal]);

  useEffect(() => {
    if (!cicloId || id) return;
    passagemService
      .consultarCiclo(cicloId)
      .then((ciclo) => {
        if (ciclo.estado === 'CONFIRMADO')
          throw new Error('Este ciclo já foi confirmado.');
        if (ciclo.terminal_pendente !== terminal)
          throw new Error('Este terminal já foi preenchido no ciclo.');
        setData(ciclo.data);
        setTurma(ciclo.turma);
        setTurno(ciclo.turno);
      })
      .catch((e: unknown) =>
        setErro(
          e instanceof Error ? e.message : 'Não foi possível retomar o ciclo.',
        ),
      )
      .finally(() => setCarregando(false));
  }, [cicloId, id, terminal]);

  const alterarEquipe = (i: number, campo: keyof EquipeMembro, valor: string) =>
    setEquipe((atual) =>
      atual.map((m, j) => (j === i ? { ...m, [campo]: valor } : m)),
    );
  const alterarLinha = (
    i: number,
    campo: 'veiculos' | 'sup_inf',
    valor: string,
  ) =>
    setLinhas((atual) =>
      atual.map((l, j) => (j === i ? { ...l, [campo]: vazio(valor) } : l)),
    );
  const alterarRadio = (
    i: number,
    campo: keyof RadioUso,
    valor: string | boolean,
  ) =>
    setRadios((atual) =>
      atual.map((r, j) =>
        j === i
          ? { ...r, [campo]: typeof valor === 'string' ? vazio(valor) : valor }
          : r,
      ),
    );

  const montarPayload = (): PassagemPayload => ({
    data,
    turma,
    turno,
    observacoes: vazio(observacoes),
    relatorio_ocorrencias: vazio(ocorrencias),
    mobile_utilizado: mobile,
    mobile_justificativa: mobile ? null : vazio(justificativa),
    equipe,
    ocupacoes_linhas: linhas,
    radios_utilizados: radios.map((r) => ({
      ...r,
      falha_descricao: r.apresentou_falha ? r.falha_descricao : null,
    })),
    detalhe:
      terminal === 'BRISAMAR'
        ? {
            ...recursos,
            eots_disponiveis: vazio(recursos.eots_disponiveis),
            eots_avariados: vazio(recursos.eots_avariados),
          }
        : !houveAtendimento
          ? { houve_atendimento: false }
          : {
              houve_atendimento: true,
              carga_mal_posicionada: cargaMalPosicionada,
              carga_mal_posicionada_descricao: cargaMalPosicionada
                ? vazio(cargaDescricao)
                : null,
              area1_atendida: areas.area1_atendida,
              area1_inicio: areas.area1_atendida
                ? vazio(areas.area1_inicio)
                : null,
              area1_termino: areas.area1_atendida
                ? vazio(areas.area1_termino)
                : null,
              area2_atendida: areas.area2_atendida,
              area2_inicio: areas.area2_atendida
                ? vazio(areas.area2_inicio)
                : null,
              area2_termino: areas.area2_atendida
                ? vazio(areas.area2_termino)
                : null,
            },
  });

  async function enviar(event: FormEvent) {
    event.preventDefault();
    setErro('');
    setEnviando(true);
    try {
      const resultado = await passagemService.salvar(
        terminal,
        montarPayload(),
        id,
      );
      if (resultado.ciclo_id) {
        if (resultado.terminal_pendente) {
          const destino =
            resultado.terminal_pendente === 'BRISAMAR' ? '/brisamar' : '/tecon';
          navigate(`${destino}?ciclo=${resultado.ciclo_id}`);
        } else {
          navigate(`/confirmacao?ciclo=${resultado.ciclo_id}`);
        }
        return;
      }
      if (id && cicloId) {
        navigate(`/confirmacao?ciclo=${cicloId}`);
        return;
      }
      const ultima: UltimaPassagem = {
        ...resultado,
        operacao: id ? 'edicao' : 'criacao',
        terminal: terminal === 'BRISAMAR' ? 'Pátio Brisamar' : 'Terminal TECON',
        data,
        turma,
        turno,
      };
      sessionStorage.setItem('ultima_passagem', JSON.stringify(ultima));
      navigate('/confirmacao');
    } catch (e) {
      setErro(
        e instanceof ApiClientError || e instanceof Error
          ? e.message
          : 'Não foi possível salvar.',
      );
    } finally {
      setEnviando(false);
    }
  }

  if (carregando)
    return (
      <main className="operation-page">
        <p className="status">Carregando passagem...</p>
      </main>
    );
  return (
    <main className="operation-page">
      <header className="operation-header">
        <Link to="/terminal">← Terminais</Link>
        <div>
          <span className="shell__eyebrow">
            {terminal === 'BRISAMAR' ? 'Pátio Brisamar' : 'Terminal TECON'}
          </span>
          <h1>{id ? 'Editar' : 'Nova'} passagem de serviço</h1>
        </div>
      </header>
      <form className="operation-form" onSubmit={enviar}>
        <Section title="Dados do turno">
          <div className="form-grid">
            <Field label="Data">
              <input
                type="date"
                required
                disabled={Boolean(id || cicloId)}
                value={data}
                onChange={(e) => setData(e.target.value)}
              />
            </Field>
            <Select
              label="Turma"
              disabled={Boolean(id || cicloId)}
              value={turma}
              onChange={(v) => setTurma(v as Turma)}
              options={['A', 'B', 'C', 'D']}
            />
            <Select
              label="Turno"
              disabled={Boolean(id || cicloId)}
              value={turno}
              onChange={(v) => setTurno(v as Turno)}
              options={['DIURNO', 'NOTURNO']}
            />
          </div>
        </Section>
        <Section title="Equipe presente">
          {equipe.map((m, i) => (
            <div className="form-grid dynamic-row" key={i}>
              <Field label="Nome">
                <input
                  required
                  value={m.nome}
                  onChange={(e) => alterarEquipe(i, 'nome', e.target.value)}
                />
              </Field>
              <Field label="Matrícula (8 dígitos)">
                <input
                  required
                  pattern="\d{8}"
                  value={m.matricula}
                  onChange={(e) =>
                    alterarEquipe(i, 'matricula', e.target.value)
                  }
                />
              </Field>
              {equipe.length > 1 && (
                <button
                  type="button"
                  className="button button--danger"
                  onClick={() => setEquipe((a) => a.filter((_, j) => j !== i))}
                >
                  Remover
                </button>
              )}
            </div>
          ))}
          <button
            type="button"
            className="button button--secondary compact"
            onClick={() => setEquipe((a) => [...a, novaEquipe()])}
          >
            Adicionar membro
          </button>
        </Section>
        <Section title="Ocupação das linhas">
          <div className="lines-grid">
            {linhas.map((l, i) => (
              <div className="line-row" key={l.codigo_linha}>
                <strong>{l.codigo_linha}</strong>
                <input
                  aria-label={`Veículos da linha ${l.codigo_linha}`}
                  placeholder="Veículos ou situação"
                  value={l.veiculos ?? ''}
                  onChange={(e) => alterarLinha(i, 'veiculos', e.target.value)}
                />
              </div>
            ))}
          </div>
        </Section>
        <Section title="Registros do turno">
          <Field label="Observações">
            <textarea
              required={terminal === 'TECON'}
              value={observacoes}
              onChange={(e) => setObservacoes(e.target.value)}
            />
          </Field>
          <Field label="Relatório de ocorrências">
            <textarea
              required={terminal === 'TECON'}
              value={ocorrencias}
              onChange={(e) => setOcorrencias(e.target.value)}
            />
          </Field>
          <Choice
            label="O Mobile foi utilizado?"
            value={mobile}
            onChange={setMobile}
          />
          {!mobile && (
            <Field label="Justificativa">
              <textarea
                required
                value={justificativa}
                onChange={(e) => setJustificativa(e.target.value)}
              />
            </Field>
          )}
        </Section>
        {terminal === 'BRISAMAR' ? (
          <Section title="Recursos entregues">
            <div className="form-grid">
              {(
                [
                  'radios_operantes',
                  'radios_inoperantes',
                  'baterias',
                  'carregadores',
                ] as const
              ).map((k) => (
                <Field key={k} label={k.replaceAll('_', ' ')}>
                  <input
                    type="number"
                    min="0"
                    required
                    value={recursos[k]}
                    onChange={(e) =>
                      setRecursos((r) => ({
                        ...r,
                        [k]: Number(e.target.value),
                      }))
                    }
                  />
                </Field>
              ))}
            </div>
            <Field label="EOTs disponíveis">
              <textarea
                value={recursos.eots_disponiveis}
                onChange={(e) =>
                  setRecursos((r) => ({
                    ...r,
                    eots_disponiveis: e.target.value,
                  }))
                }
              />
            </Field>
            <Field label="EOTs avariados">
              <textarea
                value={recursos.eots_avariados}
                onChange={(e) =>
                  setRecursos((r) => ({ ...r, eots_avariados: e.target.value }))
                }
              />
            </Field>
          </Section>
        ) : (
          <Section title="Atendimento no TECON">
            <Choice
              label="Houve atendimento?"
              value={houveAtendimento}
              onChange={setHouveAtendimento}
            />
            {houveAtendimento && (
              <>
                <Choice
                  label="Havia carga mal posicionada?"
                  value={cargaMalPosicionada}
                  onChange={setCargaMalPosicionada}
                />
                {cargaMalPosicionada && (
                  <Field label="Descrição da carga">
                    <textarea
                      required
                      value={cargaDescricao}
                      onChange={(e) => setCargaDescricao(e.target.value)}
                    />
                  </Field>
                )}
                {([1, 2] as const).map((n) => {
                  const atendida = `area${n}_atendida` as const;
                  const inicio = `area${n}_inicio` as const;
                  const termino = `area${n}_termino` as const;
                  return (
                    <div key={n} className="area-row">
                      <label>
                        <input
                          type="checkbox"
                          checked={areas[atendida]}
                          onChange={(e) =>
                            setAreas((a) => ({
                              ...a,
                              [atendida]: e.target.checked,
                            }))
                          }
                        />{' '}
                        Área {n} atendida
                      </label>
                      {areas[atendida] && (
                        <div className="form-grid">
                          <Field label="Início">
                            <input
                              type="time"
                              required
                              value={areas[inicio]}
                              onChange={(e) =>
                                setAreas((a) => ({
                                  ...a,
                                  [inicio]: e.target.value,
                                }))
                              }
                            />
                          </Field>
                          <Field label="Término">
                            <input
                              type="time"
                              required
                              value={areas[termino]}
                              onChange={(e) =>
                                setAreas((a) => ({
                                  ...a,
                                  [termino]: e.target.value,
                                }))
                              }
                            />
                          </Field>
                        </div>
                      )}
                    </div>
                  );
                })}
              </>
            )}
          </Section>
        )}
        <Section title="Rádios utilizados">
          {radios.length === 0 && (
            <p className="muted">Nenhum rádio informado.</p>
          )}
          {radios.map((r, i) => (
            <div className="radio-card" key={i}>
              <div className="form-grid">
                <Field label="Número">
                  <input
                    required
                    value={r.numero}
                    onChange={(e) => alterarRadio(i, 'numero', e.target.value)}
                  />
                </Field>
                <Field label="Manobrador">
                  <input
                    required
                    value={r.manobrador_nome}
                    onChange={(e) =>
                      alterarRadio(i, 'manobrador_nome', e.target.value)
                    }
                  />
                </Field>
                <Field label="Retirada">
                  <input
                    type="time"
                    value={r.hora_retirada ?? ''}
                    onChange={(e) =>
                      alterarRadio(i, 'hora_retirada', e.target.value)
                    }
                  />
                </Field>
                <Field label="Entrega">
                  <input
                    type="time"
                    value={r.hora_entrega ?? ''}
                    onChange={(e) =>
                      alterarRadio(i, 'hora_entrega', e.target.value)
                    }
                  />
                </Field>
              </div>
              <label>
                <input
                  type="checkbox"
                  checked={r.apresentou_falha}
                  onChange={(e) =>
                    alterarRadio(i, 'apresentou_falha', e.target.checked)
                  }
                />{' '}
                Apresentou falha
              </label>
              {r.apresentou_falha && (
                <Field label="Descrição da falha">
                  <textarea
                    required
                    value={r.falha_descricao ?? ''}
                    onChange={(e) =>
                      alterarRadio(i, 'falha_descricao', e.target.value)
                    }
                  />
                </Field>
              )}
              <button
                type="button"
                className="button button--danger compact"
                onClick={() => setRadios((a) => a.filter((_, j) => j !== i))}
              >
                Remover rádio
              </button>
            </div>
          ))}
          <button
            type="button"
            className="button button--secondary compact"
            onClick={() => setRadios((a) => [...a, novoRadio()])}
          >
            Adicionar rádio
          </button>
        </Section>
        {erro && (
          <p role="alert" className="status status--error">
            {erro}
          </p>
        )}
        <button
          className="button submit-button"
          disabled={enviando}
          type="submit"
        >
          {enviando
            ? 'Enviando...'
            : id
              ? 'Salvar alterações'
              : 'Enviar passagem de serviço'}
        </button>
      </form>
    </main>
  );
}

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section className="form-section">
      <h2>{title}</h2>
      {children}
    </section>
  );
}
function Field({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <label className="field">
      <span>{label}</span>
      {children}
    </label>
  );
}
function Select({
  label,
  value,
  onChange,
  options,
  disabled,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  options: string[];
  disabled?: boolean;
}) {
  return (
    <Field label={label}>
      <select
        disabled={disabled}
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        {options.map((o) => (
          <option key={o}>{o}</option>
        ))}
      </select>
    </Field>
  );
}
function Choice({
  label,
  value,
  onChange,
}: {
  label: string;
  value: boolean;
  onChange: (v: boolean) => void;
}) {
  return (
    <fieldset className="choice">
      <legend>{label}</legend>
      <label>
        <input type="radio" checked={value} onChange={() => onChange(true)} />{' '}
        Sim
      </label>
      <label>
        <input type="radio" checked={!value} onChange={() => onChange(false)} />{' '}
        Não
      </label>
    </fieldset>
  );
}
