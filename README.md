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
| Frontend atual | HTML, CSS e JavaScript |
| Autenticação | JWT, Passlib e bcrypt |
| Qualidade | Pytest, pytest-cov, Ruff, mypy e pre-commit |
| Dependências | `pyproject.toml`, `uv` e `uv.lock` |

## Subir o projeto no Windows

### 1. Pré-requisitos

- Git;
- Python 3.13;
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

### 6. Iniciar o frontend

Abra outro PowerShell na raiz do projeto:

```powershell
py -3.13 -m uv run python -m http.server 3000 --directory frontend
```

Acesse `http://127.0.0.1:3000`. Não abra os arquivos HTML diretamente pelo
Explorer; o servidor HTTP evita diferenças de origem e carregamento.

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

Estado validado deste checkpoint:

- 105 testes aprovados;
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
│   ├── alembic.ini
│   └── main.py               # entrypoint compatível temporário
├── frontend/                 # interface legada HTML/CSS/JavaScript
├── docs/                     # arquitetura, padrões, tasks e checkpoint
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
- **Frontend não conecta:** confirme que a API está em `127.0.0.1:8000` e o
  frontend em `127.0.0.1:3000`.
- **CORS no navegador:** confira se a origem exata do frontend está em
  `CORS_ORIGINS`.
- **Banco vazio:** aplique `alembic upgrade head` e prepare um usuário de teste.

## Limitações atuais e próximos passos

- frontend ainda é HTML/CSS/JavaScript e será migrado incrementalmente para
  React + TypeScript;
- ainda não há Docker, CI remoto ou deploy público;
- contrato unificado de erros e reorganização backend por feature são as
  próximas etapas técnicas;
- consultas com filtros, exportações e relatórios permanecem no roadmap.

O estado seguro e a retomada do desenvolvimento estão em
[`docs/CHECKPOINT.md`](docs/CHECKPOINT.md).

## Documentação e autoria

A documentação técnica deste repositório está em [`docs/`](docs/README.md). A
documentação de requisitos e protótipos também está disponível no repositório
[`railops-docs`](https://github.com/ChoqueanoIV/railops-docs).

Desenvolvido por [Leandro](https://github.com/ChoqueanoIV) como projeto de
portfólio para transição de carreira em desenvolvimento de software.
