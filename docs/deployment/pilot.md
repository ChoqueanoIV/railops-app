# Piloto público gratuito

Este runbook publica uma demonstração do RailOps sem dados operacionais reais,
sem custo contratado e sem tratá-la como produção.

## Limites aprovados

- somente identidades e passagens fictícias;
- URL pública compartilhada com testadores convidados;
- nenhum cartão, upgrade ou cobrança automática;
- indisponibilidade e inicialização lenta dos planos gratuitos são aceitas;
- qualquer uso operacional exige novo gate de privacidade, retenção e backup.

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
5. Não importe dados cotidianos nem execute o seed E2E.

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

`public/_redirects` preserva rotas React abertas diretamente ou recarregadas.

## Usuários e homologação

Cadastre apenas matrículas fictícias por procedimento administrativo. O seed
E2E é bloqueado fora do banco E2E e não deve ser adaptado para este piloto.

Valide `/health`, `/ready`, primeiro acesso, login, ciclo completo, confirmação,
consulta, permissões e downloads com os três perfis fictícios. Confirme que URL,
tela, logs e arquivos não expõem PIN, código, JWT ou conexão do banco.

## Backup e recuperação

O Supabase Free não oferece backup automático. Antes de migrations ou rodadas
relevantes, produza dump lógico pela CLI do Supabase ou `pg_dump`, mantenha-o
fora do repositório e teste sua restauração em banco descartável. Como só há
dados fictícios, também é aceitável recriar o banco e reaplicar migrations.

## Operação e retirada

- merges na `main` podem disparar deploy após os checks do PR;
- suspensão e latência do plano grátis não justificam reduzir segurança;
- pause o serviço nos painéis para interromper o piloto;
- só exclua o banco após confirmar que contém exclusivamente dados fictícios;
- exclusão de projeto é irreversível.
