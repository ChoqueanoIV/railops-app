# Piloto público gratuito

Este runbook mantém um piloto operacional controlado do Passagem de Turno
Digital, sem custo contratado e sem tratá-lo como ambiente definitivo de
produção. O uso cotidiano foi autorizado por período inicial de um a dois
meses para coleta de dados e avaliação na operação.

## Limites aprovados

- somente usuários previamente autorizados e identificados;
- dados operacionais limitados ao escopo da passagem de turno do piloto;
- URL pública compartilhada apenas com participantes convidados;
- nenhum cartão, upgrade ou cobrança automática;
- indisponibilidade e inicialização lenta dos planos gratuitos são aceitas;
- a autorização do piloto não equivale à homologação corporativa definitiva;
- expansão de público, prazo, finalidade ou integração exige novo gate de
  privacidade, retenção, backup e aderência às políticas da MRS.

## Arquitetura

| Camada | Serviço | Plano |
|---|---|---|
| React estático | Cloudflare Pages | Free |
| FastAPI em container | Render Web Service | Free |
| PostgreSQL | Supabase | Free |

O navegador acessa o frontend e a API. A conexão PostgreSQL fica somente nas
variáveis secretas do Render.

## Provisionamento

### Banco Supabase

1. Crie um projeto Free exclusivo para o piloto.
2. Guarde a senha em um gerenciador de senhas.
3. Em **Connect**, copie a URI do pooler em modo de sessão (IPv4).
4. Use TLS, acrescentando `sslmode=require` se necessário.
5. Nunca execute o seed E2E neste banco. Cadastros e dados cotidianos devem
   respeitar exclusivamente o escopo autorizado do piloto.

### API Render

1. Escolha **New > Blueprint**, conecte o repositório e use `render.yaml`.
2. Preencha `DATABASE_URL` com a URI do Supabase.
3. Preencha `CORS_ORIGINS` com a URL exata do Cloudflare Pages; nunca use `*`.
4. Aguarde `/ready` responder `200` com estado `ok`.

O serviço executa `backend/scripts/start_render.sh`, que aplica
`alembic upgrade head` antes do Uvicorn. O fluxo fica na inicialização porque
pre-deploy separado não integra o plano Free.

### React no Cloudflare Pages

| Campo | Valor |
|---|---|
| Branch | `main` |
| Diretório raiz | `frontend/react` |
| Build | `npm ci && npm run build` |
| Saída | `dist` |
| `VITE_API_BASE_URL` | URL HTTPS da API Render, sem barra final |

O Pages aplica seu fallback nativo de SPA porque o artefato não possui uma
página `404.html`; assim, rotas React abertas diretamente ou recarregadas
continuam resolvendo para `index.html` sem uma regra `_redirects` redundante.

## Usuários e homologação

Cadastre somente matrículas expressamente autorizadas, por procedimento
administrativo. Não registre matrículas, códigos de ativação, PINs ou hashes no
repositório. O seed E2E é bloqueado fora do banco E2E e não deve ser adaptado
para este piloto.

Somente `MANOBRADOR` cria, edita e confirma passagens. `INSTRUTOR` e
`MONITOR_QUALIDADE` ficam restritos à consulta, auditoria e exportações já
autorizadas. Valide `/health`, `/ready`, primeiro acesso, login, ciclo completo,
confirmação, consulta, permissões e downloads. Confirme que URL, tela, logs e
arquivos não expõem PIN, código, JWT ou conexão do banco.

## Backup e recuperação

O Supabase Free não oferece backup automático. Antes de migrations ou rodadas
relevantes, produza dump lógico pela CLI do Supabase ou `pg_dump`, mantenha-o
fora do repositório e teste sua restauração em banco descartável. A cópia
temporária `pilot_backup_20260914`, criada antes da limpeza dos dados de
homologação, é isolada dos papéis públicos, mas não substitui um backup externo
testado nem deve ser mantida além do prazo necessário.

## Operação e retirada

- merges na `main` podem disparar deploy após os checks do PR;
- suspensão e latência do plano grátis não justificam reduzir segurança;
- pause o serviço nos painéis para interromper o piloto;
- não exclua o banco ou dados operacionais sem inventário, cópia recuperável e
  autorização explícita;
- exclusão de projeto é irreversível.
