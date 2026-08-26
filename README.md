# RailOps

Sistema web para digitalizar a passagem de serviço entre turnos no Pátio
Brisamar e no Terminal TECON, preservando as regras operacionais existentes.

> **Status:** MVP funcional, testado e com CI. Login, primeiro acesso, seleção
> de terminal, criação, edição e confirmação de passagens estão disponíveis no
> React. A API preserva o estado anterior de cada edição. Ainda não há deploy
> público nem telas dedicadas para histórico, filtros ou relatórios.

## Funcionalidades disponíveis

- primeiro acesso com matrícula, código de ativação e definição de PIN;
- login JWT e rotas protegidas;
- passagens específicas para Brisamar e TECON;
- data operacional baseada no início do turno, inclusive no turno noturno;
- validações de domínio e janela de edição no backend;
- confirmação do registro e histórico persistido das edições;
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
centralizada. Os HTML/CSS/JavaScript anteriores permanecem apenas como fallback
durante a validação operacional.

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
JWT_SECRET_KEY=exemplo-local-substitua-por-um-segredo-longo
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

1. Confirme `/health` e abra `/docs`.
2. Conclua primeiro acesso e login no React.
3. Registre e confirme uma passagem válida de Brisamar.
4. Edite-a dentro da janela permitida.
5. Repita o fluxo para TECON e valide os campos das Áreas 1 e 2.
6. Envie combinações condicionais inválidas e confira as mensagens da API.

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

Estado validado neste checkpoint:

- backend: 123 testes e cobertura real de 93,70% (94% arredondado);
- frontend: 13 testes;
- formatter, lint, type-check, build e pre-commit aprovados;
- CI executa jobs independentes de backend e frontend em PRs e na `main`.

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
│   ├── react/src/
│   │   ├── app/             # bootstrap e rotas
│   │   ├── features/        # auth, shell e passagens
│   │   ├── services/        # cliente da API
│   │   └── test/            # setup dos testes
│   ├── css/ e js/           # fallback legado temporário
│   └── *.html               # fallback legado temporário
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
- **Banco vazio:** aplique as migrations e prepare o usuário de demonstração.

## Roadmap

Concluído: caracterização das regras, arquitetura por features, contratos de
erro, dependências reproduzíveis, testes, qualidade estática, Docker, fluxos
React e CI.

Planejado, ainda não concluído:

- hardening final e limpeza segura dos adaptadores/fallbacks;
- validação operacional e de UX com usuários;
- consulta de histórico, filtros, exportações e relatórios;
- estratégia de deploy e observabilidade.

O estado de retomada fica em [`docs/CHECKPOINT.md`](docs/CHECKPOINT.md), o índice
técnico em [`docs/README.md`](docs/README.md) e o backlog em
[`docs/tasks/README.md`](docs/tasks/README.md).

## Autoria

Desenvolvido por [Leandro](https://github.com/ChoqueanoIV) como projeto de
portfólio para transição de carreira. Requisitos e protótipos originais estão
no [`railops-docs`](https://github.com/ChoqueanoIV/railops-docs).
