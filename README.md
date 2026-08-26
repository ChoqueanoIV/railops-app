# RailOps

Sistema web para digitalizar a passagem de serviço entre turnos na operação
ferroviária do Pátio Brisamar e do Terminal TECON.

> **Status:** MVP funcional em evolução. Login, primeiro acesso, passagens de
> Brisamar e TECON, edição e histórico já estão implementados. Ainda não há
> deploy público nem pipeline de CI.

## O que já pode ser testado

- primeiro acesso por matrícula, código de ativação e definição de PIN;
- login com token JWT;
- seleção do Pátio Brisamar ou Terminal TECON;
- criação de passagem de serviço para os dois terminais;
- validações operacionais específicas de Brisamar e TECON;
- edição da passagem dentro da janela permitida;
- preservação do estado anterior no histórico;
- API documentada por Swagger/OpenAPI;
- persistência PostgreSQL com migrations Alembic.

## Stack

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.13, FastAPI e Pydantic |
| Persistência | PostgreSQL, SQLAlchemy e Alembic |
| Frontend | React + TypeScript (shell) e HTML/CSS/JavaScript (fluxos legados) |
| Autenticação | JWT, Passlib e bcrypt |
| Qualidade | Pytest, pytest-cov, Ruff, mypy e pre-commit |
| Dependências | `pyproject.toml`, `uv` e `uv.lock` |

## Subir com Docker Compose

Esse é o caminho mais curto para executar API e PostgreSQL localmente. Instale
Docker Desktop com suporte ao Compose e, na raiz do repositório, crie o arquivo
de variáveis local:

```powershell
Copy-Item .env.docker.example .env.docker
```

Substitua `POSTGRES_PASSWORD` e `JWT_SECRET_KEY` em `.env.docker`. Use uma senha
de banco compatível com URL (sem caracteres que precisem de codificação) e
nunca versione esse arquivo. Depois execute:

```powershell
docker compose --env-file .env.docker up --build -d
docker compose --env-file .env.docker ps
```

O PostgreSQL precisa ficar saudável antes do backend. Ao iniciar, o backend
executa `alembic upgrade head` e somente então abre a API como usuário não-root.
Confira:

- health check: `http://127.0.0.1:8000/health`;
- Swagger: `http://127.0.0.1:8000/docs`;
- logs: `docker compose --env-file .env.docker logs -f backend`.

Para encerrar sem apagar os dados:

```powershell
docker compose --env-file .env.docker down
```

O volume `railops_postgres_data` preserva o banco. Use `down -v` somente quando
quiser apagar deliberadamente todos os dados locais do PostgreSQL.

Esse fluxo foi validado com Docker Engine 29.7.2 e Compose v5.4.0: banco e API
ficaram saudáveis, as migrations chegaram ao `head` e Swagger respondeu HTTP
200.

## Subir o projeto no Windows

### 1. Pré-requisitos

- Git;
- Python 3.13;
- Node.js 24 e npm 11;
- PostgreSQL acessível, local ou hospedado;
- PowerShell.

Clone o repositório:

```powershell
git clone https://github.com/ChoqueanoIV/railops-app.git
Set-Location railops-app
```

### 2. Instalar o uv e as dependências

Instale o `uv` no perfil do usuário:

```powershell
py -3.13 -m pip install --user uv
```

Reabra o terminal caso o comando não seja localizado. Na raiz do projeto,
reconstrua o ambiente usando as versões exatas do lockfile:

```powershell
py -3.13 -m uv sync --frozen
```

### 3. Configurar o ambiente

Crie o arquivo local a partir do exemplo:

```powershell
Copy-Item backend\.env.example backend\.env
```

Preencha `backend/.env`:

```dotenv
DATABASE_URL=postgresql://usuario:senha@host:5432/railops
JWT_SECRET_KEY=substitua-por-um-segredo-longo-e-aleatorio
RAILOPS_ENV=development
API_TITLE=RailOps API
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

Para Supabase ou outro PostgreSQL que exija TLS, a URL normalmente precisa do
parâmetro `sslmode=require`. Use as informações fornecidas pelo seu provedor.

Nunca envie o `.env` por Git, commit, print ou mensagem pública. Para permitir
que outra pessoa avalie o sistema, forneça credenciais de um banco descartável
por um canal privado.

### 4. Aplicar as migrations

Na raiz do repositório:

```powershell
py -3.13 -m uv --directory backend run alembic upgrade head
```

Esse comando cria e atualiza as tabelas e também registra as linhas
operacionais usadas por Brisamar e TECON.

### 5. Iniciar o backend

```powershell
py -3.13 -m uv run uvicorn app.main:app --reload --app-dir backend
```

Verifique:

- API: `http://127.0.0.1:8000`;
- health check: `http://127.0.0.1:8000/health`;
- Swagger: `http://127.0.0.1:8000/docs`;
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`.

O health check deve responder:

```json
{"status": "ok"}
```

### 6. Iniciar o frontend legado

Abra outro PowerShell na raiz do projeto:

```powershell
py -3.13 -m uv run python -m http.server 3000 --directory frontend
```

Acesse `http://127.0.0.1:3000`. Não abra os arquivos HTML diretamente pelo
Explorer; o servidor HTTP evita diferenças de origem e carregamento.

### 7. Iniciar o shell React

O shell moderno é independente dos fluxos legados. Em outro PowerShell:

```powershell
Set-Location frontend\react
npm ci
Copy-Item .env.example .env.local
npm run dev
```

Acesse `http://127.0.0.1:5173`. O React já oferece login, primeiro acesso e
proteção da rota inicial usando os contratos atuais da API. As telas
operacionais de Brisamar e TECON continuam no frontend legado até a migração
incremental. Para validar a qualidade do frontend moderno:

```powershell
npm run lint
npm run typecheck
npm test
npm run build
```

## Criar um usuário para avaliação

As migrations não criam usuários. Se o avaliador estiver usando um banco local
ou descartável, o comando abaixo cria ou reinicia um usuário de demonstração:

```powershell
@'
from app.core.database import SessionLocal
from app.models.usuario import Usuario
from app.services.auth_service import pwd_context

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

Use somente em banco local ou de teste. Depois:

1. abra `http://127.0.0.1:3000`;
2. clique em **Definir meu PIN**;
3. informe matrícula `12345678`;
4. informe código de ativação `123456`;
5. escolha e confirme um PIN de quatro dígitos;
6. volte ao login e entre com a matrícula e o novo PIN.

Se for utilizado um banco compartilhado já preparado, peça ao responsável uma
matrícula e um código de ativação ou PIN por canal privado e ignore esta etapa.

## Roteiro de avaliação manual

1. Confirme `/health` e abra `/docs`.
2. Realize o primeiro acesso e o login pelo frontend.
3. Entre em Brisamar e registre uma passagem válida.
4. Confira a tela de confirmação.
5. Edite a passagem dentro da janela operacional permitida.
6. Repita o fluxo para TECON e valide os campos específicos das Áreas 1 e 2.
7. Tente enviar dados condicionais inválidos para observar as validações.

As regras atuais estão congeladas e descritas em
[`docs/architecture/baseline.md`](docs/architecture/baseline.md).

## Testes e qualidade

Execute a suíte completa:

```powershell
py -3.13 -m uv run pytest
```

Execute todos os checks:

```powershell
py -3.13 -m uv run pytest --cov=backend/app --cov-report=term-missing
py -3.13 -m uv run ruff check .
py -3.13 -m uv run ruff format --check .
py -3.13 -m uv run mypy
py -3.13 -m uv run pre-commit run --all-files
```

Para o shell React, execute os comandos dentro de `frontend/react`:

```powershell
npm run lint
npm run format:check
npm run typecheck
npm test
npm run build
```

Estado validado deste checkpoint:

- 120 testes aprovados;
- cobertura total de 94%;
- lint, formatter, type-check e pre-commit aprovados.

## Estrutura do repositório

```text
railops-app/
├── backend/
│   ├── alembic/              # migrations do PostgreSQL
│   ├── app/
│   │   ├── core/             # configuração tipada e banco
│   │   ├── models/           # modelos SQLAlchemy
│   │   ├── repositories/     # persistência
│   │   ├── routers/          # endpoints FastAPI
│   │   ├── schemas/          # contratos Pydantic
│   │   ├── services/         # regras de negócio
│   │   └── main.py           # fábrica e bootstrap da aplicação
│   ├── tests/                # testes automatizados
│   ├── .env.example
│   ├── Dockerfile
│   ├── alembic.ini
│   └── main.py               # entrypoint compatível temporário
├── frontend/
│   ├── react/                # shell React + TypeScript isolado
│   ├── css/                  # estilos legados
│   ├── js/                   # scripts legados
│   └── *.html                # telas legadas ainda operacionais
├── docs/                     # arquitetura, padrões, tasks e checkpoint
├── compose.yaml              # API e PostgreSQL para desenvolvimento local
├── pyproject.toml            # manifesto e ferramentas Python
├── uv.lock                   # versões reproduzíveis
└── README.md
```

## Compatibilidade com pip

O fluxo recomendado usa `uv`. Para ferramentas que ainda exigem `pip`, os
requirements são exports gerados do mesmo lockfile:

```powershell
py -3.13 -m venv .venv
.venv\Scripts\python.exe -m pip install --require-hashes -r backend\requirements-dev.txt
```

Não edite `backend/requirements.txt` ou `backend/requirements-dev.txt`
manualmente.

## Solução de problemas

- **Python bloqueado dentro do OneDrive:** mova o clone para uma pasta local não
  sincronizada e execute `uv sync --frozen` novamente.
- **Erro de `DATABASE_URL`:** confira `backend/.env`, host, porta, nome do banco e
  exigência de TLS.
- **Erro de `JWT_SECRET_KEY`:** defina uma chave não vazia no `.env`.
- **Frontend não conecta:** confirme que a API está em `127.0.0.1:8000`, o
  legado em `127.0.0.1:3000` ou o React em `127.0.0.1:5173` e confira
  `frontend/react/.env.local`.
- **CORS no navegador:** confira se a origem exata do frontend está em
  `CORS_ORIGINS`.
- **Banco vazio:** aplique `alembic upgrade head` e prepare um usuário de teste.
- **Compose não inicia:** confirme Docker Desktop ativo, revise `.env.docker` e
  execute `docker compose --env-file .env.docker logs backend db`.

## Limitações atuais e próximos passos

- login, primeiro acesso, seleção de terminal, passagens de Brisamar e TECON,
  edição e confirmação já estão disponíveis no React;
- o frontend legado permanece versionado como fallback temporário até a
  validação operacional das telas React;
- a configuração Docker e o CI remoto existem, mas ainda não há deploy
  público;
- consolidação do README e da documentação final é a próxima etapa técnica;
- consultas com filtros, exportações e relatórios permanecem no roadmap.

O estado seguro e a retomada do desenvolvimento estão em
[`docs/CHECKPOINT.md`](docs/CHECKPOINT.md).

## Documentação e autoria

A documentação técnica deste repositório está em [`docs/`](docs/README.md). A
documentação de requisitos e protótipos também está disponível no repositório
[`railops-docs`](https://github.com/ChoqueanoIV/railops-docs).

Desenvolvido por [Leandro](https://github.com/ChoqueanoIV) como projeto de
portfólio para transição de carreira em desenvolvimento de software.
