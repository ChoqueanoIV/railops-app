# RailOps

Sistema web para digitalizar a passagem de serviço entre turnos no Pátio
Brisamar e no Terminal TECON, preservando as regras operacionais existentes.

> **Status:** piloto funcional, publicado e homologado com dados fictícios.
> Login, primeiro acesso, ciclo Brisamar + TECON, revisão, confirmação, consulta,
> histórico e exportações estão disponíveis no React. Backend, Frontend, E2E e
> deploy são validados continuamente pela CI.

## Piloto público

- aplicação: <https://railops-piloto.pages.dev/login>;
- API: <https://railops-api-piloto.onrender.com>;
- finalidade: demonstração e homologação por testadores convidados;
- dados permitidos: exclusivamente identidades e passagens fictícias.

O piloto usa Cloudflare Pages Free, Render Free e Supabase Free. A primeira
requisição à API pode levar cerca de 50 segundos quando o Render estiver
suspenso por inatividade. O ambiente não possui SLA nem backup automático e não
deve ser usado em uma operação ferroviária real. Credenciais fictícias de teste
são compartilhadas privadamente pelo responsável do projeto e nunca ficam
versionadas no repositório.

## Funcionalidades disponíveis

- primeiro acesso com matrícula, código de ativação e definição de PIN;
- login JWT e rotas protegidas;
- passagens específicas para Brisamar e TECON;
- data operacional baseada no início do turno, inclusive no turno noturno;
- validações de domínio e janela de edição no backend;
- confirmação do registro e histórico persistido das edições;
- consulta filtrada e paginada das passagens confirmadas;
- histórico visual restrito a Instrutores e Monitores de Qualidade;
- PDF individual e exportações consolidadas em PDF e CSV;
- PostgreSQL versionado por migrations Alembic;
- Swagger/OpenAPI, testes automatizados e GitHub Actions.

As regras protegidas pela caracterização estão em
[`docs/architecture/baseline.md`](docs/architecture/baseline.md).

## Arquitetura e stack

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.13, FastAPI e Pydantic |
| Persistência | PostgreSQL, SQLAlchemy e Alembic |
| Frontend | React 19, TypeScript, Vite e React Router |
| Autenticação | JWT, Passlib e bcrypt |
| Qualidade | Pytest, Vitest, Testing Library, Ruff, mypy, ESLint e Prettier |
| Automação | Docker Compose, pre-commit e GitHub Actions |
| Dependências | `pyproject.toml`, `uv.lock` e `package-lock.json` |

O backend está organizado por features (`auth` e `passagens`) e mantém
adaptadores temporários para imports antigos. O React usa uma API tipada e
centralizada e é a única interface web mantida no repositório. O frontend
estático anterior foi removido após homologação local, automatizada e pública.

## Execução rápida com Docker

Esse fluxo sobe PostgreSQL e API. O React é iniciado separadamente.

### Requisitos

- Git;
- Docker Desktop com Docker Compose;
- Node.js 24 e npm 11 para o frontend.

Na raiz do clone:

```powershell
Copy-Item .env.docker.example .env.docker
```

Substitua `POSTGRES_PASSWORD` e `JWT_SECRET_KEY` em `.env.docker`. Nunca
versione esse arquivo. Depois:

```powershell
docker compose --env-file .env.docker up --build -d
docker compose --env-file .env.docker ps
```

O backend aguarda o banco, aplica `alembic upgrade head` e inicia como usuário
não-root. Verifique:

- health: `http://127.0.0.1:8000/health`;
- readiness do banco: `http://127.0.0.1:8000/ready`;
- Swagger: `http://127.0.0.1:8000/docs`;
- logs: `docker compose --env-file .env.docker logs -f backend`.

Para parar sem apagar o banco:

```powershell
docker compose --env-file .env.docker down
```

O volume `railops_postgres_data` preserva os dados. `down -v` também apaga o
volume e deve ser usado somente quando essa perda for intencional.

## Execução local no Windows

### 1. Requisitos e dependências

- Git, Python 3.13, PostgreSQL, Node.js 24, npm 11 e PowerShell;
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/).

```powershell
git clone https://github.com/ChoqueanoIV/railops-app.git
Set-Location railops-app
py -3.13 -m pip install --user uv
py -3.13 -m uv sync --frozen
```

O último comando usa as versões exatas de `uv.lock`.

### 2. Configurar backend e banco

```powershell
Copy-Item backend\.env.example backend\.env
```

Use valores locais ou de um banco descartável:

```dotenv
DATABASE_URL=postgresql://railops_local:senha-falsa@localhost:5432/railops
JWT_SECRET_KEY=exemplo-local-substitua-por-32-bytes-ou-mais
RAILOPS_ENV=development
API_TITLE=RailOps API
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Provedores que exigem TLS normalmente requerem `sslmode=require` na URL.
Mantenha `.env`, credenciais e capturas com segredos fora do Git.

### 3. Aplicar migrations e iniciar a API

```powershell
py -3.13 -m uv --directory backend run alembic upgrade head
py -3.13 -m uv run uvicorn app.main:app --reload --app-dir backend
```

- API: `http://127.0.0.1:8000`;
- health: `http://127.0.0.1:8000/health`;
- readiness do banco: `http://127.0.0.1:8000/ready`;
- Swagger: `http://127.0.0.1:8000/docs`;
- OpenAPI: `http://127.0.0.1:8000/openapi.json`.

### 4. Iniciar o frontend React

Em outro PowerShell:

```powershell
Set-Location frontend\react
npm ci
Copy-Item .env.example .env.local
npm run dev
```

Acesse `http://127.0.0.1:5173`. O `.env.local` aponta por padrão para a API em
`http://127.0.0.1:8000`.

## Criar usuário de demonstração

As migrations não criam usuários. Em banco exclusivamente local ou de teste:

```powershell
@'
from app.core.database import SessionLocal
from app.features.auth.models import Usuario
from app.features.auth.service import pwd_context

matricula = "12345678"
codigo_ativacao = "123456"

with SessionLocal() as db:
    usuario = db.query(Usuario).filter(Usuario.matricula == matricula).one_or_none()
    if usuario is None:
        usuario = Usuario(matricula=matricula, nome="Avaliador RailOps")
        db.add(usuario)
    usuario.senha_hash = None
    usuario.pin_definido = False
    usuario.codigo_ativacao_hash = pwd_context.hash(codigo_ativacao)
    db.commit()

print("Usuário de demonstração preparado.")
'@ | py -3.13 -m uv --directory backend run python -
```

No React, escolha **Definir meu PIN**, informe matrícula `12345678`, código
`123456`, defina um PIN de quatro dígitos e use-o no login. Não execute esse
script em produção ou banco compartilhado.

## Roteiro de teste manual

1. Faça login no React com uma identidade fictícia fornecida pelo responsável.
2. Comece por Brisamar ou TECON e preencha somente informações inventadas.
3. No Brisamar, valide L22/L24 superior, inferior e travessão simultaneamente.
4. Conclua o outro terminal dentro do mesmo ciclo.
5. Revise os dois terminais, faça uma correção e confirme definitivamente.
6. Tente editar após a confirmação e confira o bloqueio.
7. Consulte a passagem, aplique filtros e baixe o PDF individual.
8. Com os perfis autorizados, valide histórico e consolidados PDF/CSV; o
   Manobrador deve receber 403 nesses recursos sem perder a sessão.

## Testes e qualidade

Na raiz:

```powershell
py -3.13 -m uv run pytest --cov=backend/app --cov-report=term-missing --cov-fail-under=90
py -3.13 -m uv run ruff check backend
py -3.13 -m uv run ruff format --check backend
py -3.13 -m uv run mypy backend
py -3.13 -m uv run pre-commit run --all-files
```

Em `frontend/react`:

```powershell
npm test
npm run format:check
npm run lint
npm run typecheck
npm run build
```

Para executar os testes E2E, mantenha o Docker Desktop ativo e use, também em
`frontend/react`:

```powershell
npx playwright install chromium
npm run test:e2e
```

O comando cria um PostgreSQL temporário e uma API exclusivos do projeto
`railops-e2e`, aplica as migrations, prepara somente fixtures fictícias, executa
o Chromium e remove containers, rede e dados temporários ao final. Ele não usa
nem apaga o volume do ambiente cotidiano. Para diagnóstico interativo, use
`npm run test:e2e:ui`.

Estado validado neste checkpoint:

- backend: 177 testes;
- frontend: 28 testes;
- 6 cenários E2E aprovados no Chromium contra API e PostgreSQL isolados;
- formatter, lint, type-check, build e pre-commit aprovados;
- CI executa jobs independentes de Backend, Frontend e E2E em PRs e na `main`;
- piloto público homologado com os três perfis e rotas diretas do React;
- frontend estático anterior removido após homologação, sem alterar contratos.

Cada resposta inclui `X-Request-ID` e headers defensivos. A API escreve logs
JSON com metadados operacionais, sem payloads, PINs, tokens ou credenciais. Em
`production`, o segredo JWT deve possuir pelo menos 32 bytes e CORS não aceita
`*`.

## Estrutura do repositório

```text
railops-app/
├── .github/workflows/       # pipeline de qualidade
├── backend/
│   ├── alembic/             # migrations PostgreSQL
│   ├── app/
│   │   ├── api/             # respostas HTTP compartilhadas
│   │   ├── core/            # configuração e banco
│   │   ├── features/        # auth e passagens por domínio
│   │   ├── shared/          # infraestrutura compartilhada
│   │   ├── models/          # adaptadores de compatibilidade
│   │   ├── repositories/    # adaptadores de compatibilidade
│   │   ├── routers/         # adaptadores de compatibilidade
│   │   ├── schemas/         # adaptadores de compatibilidade
│   │   ├── services/        # adaptadores de compatibilidade
│   │   └── main.py          # fábrica da aplicação
│   ├── tests/               # unitários, integração e API
│   └── Dockerfile
├── frontend/
│   └── react/
│       ├── src/
│       │   ├── app/         # bootstrap e rotas
│       │   ├── features/    # auth, shell e passagens
│       │   ├── services/    # cliente da API
│       │   └── test/        # setup dos testes
│       ├── e2e/              # fluxos reais no Chromium
│       └── package.json      # scripts e dependências do frontend
├── docs/                    # arquitetura, padrões, tasks e checkpoint
├── compose.yaml
├── pyproject.toml
├── uv.lock
└── README.md
```

## Fluxo Git e CI

O projeto usa uma branch curta por task, commits semânticos e pull request para
`main`. Antes do merge, o CI valida testes, cobertura, formatação, lint,
type-check e build. Veja [`docs/standards/git.md`](docs/standards/git.md).

## Compatibilidade com pip

O fluxo recomendado usa `uv`. Os requirements com hashes são exports do mesmo
lockfile para ferramentas que exigem `pip`:

```powershell
py -3.13 -m venv .venv
.venv\Scripts\python.exe -m pip install --require-hashes -r backend\requirements-dev.txt
```

Não edite `backend/requirements*.txt` manualmente.

## Solução de problemas

- **Executáveis bloqueados no OneDrive:** pause a sincronização ou mantenha o
  clone em pasta não sincronizada; depois execute `uv sync --frozen`.
- **Falha de banco:** confira `DATABASE_URL` e aplique `alembic upgrade head`.
- **Falha de CORS:** inclua exatamente `localhost:5173` ou `127.0.0.1:5173` em
  `CORS_ORIGINS` e reinicie a API.
- **Frontend sem API:** confira `VITE_API_BASE_URL` e o health da porta 8000.
- **Compose não sobe:** confirme Docker Desktop ativo e consulte
  `docker compose --env-file .env.docker logs backend db`.
- **Socket temporário do Docker bloqueado:** encerre o Docker Desktop e reinicie
  o Windows antes de considerar qualquer reset; não use “factory reset” sem um
  backup explícito dos volumes.
- **Banco vazio:** aplique as migrations e prepare o usuário de demonstração.

## Roadmap

Concluído: caracterização das regras, arquitetura por features, contratos de
erro, dependências reproduzíveis, Docker, React, consulta, histórico,
exportações, CI, E2E, piloto público gratuito e remoção segura do frontend
estático anterior.

Próximas evoluções dependem de feedback e de aprovação explícita de um novo
gate. Possibilidades ainda não autorizadas incluem:

- melhorias de usabilidade identificadas por testadores;
- administração segura de usuários e perfis;
- monitoramento, backup e recuperação adequados para uso real;
- novos terminais e relatórios, somente após validação das regras;
- preparação de infraestrutura de produção com segurança, retenção e SLA.

O estado de retomada fica em [`docs/CHECKPOINT.md`](docs/CHECKPOINT.md), o índice
técnico em [`docs/README.md`](docs/README.md) e o backlog em
[`docs/tasks/README.md`](docs/tasks/README.md).

## Autoria

Desenvolvido por [Leandro](https://github.com/ChoqueanoIV) como projeto de
portfólio para transição de carreira. Requisitos e protótipos originais estão
no [`railops-docs`](https://github.com/ChoqueanoIV/railops-docs).
