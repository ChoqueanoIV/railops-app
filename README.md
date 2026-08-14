# RailOps

Sistema web para digitalizar a passagem de serviço entre turnos na operação
ferroviária do Pátio Brisamar e do Terminal TECON.

> **Status:** Fase 9 — implementação em andamento. Autenticação, passagem do
> Brisamar e passagem do TECON estão implementadas. O projeto ainda não possui
> uma versão implantada em produção.

## Sobre o projeto

O processo original é preenchido em papel e arquivado fisicamente, o que
dificulta consultas, histórico e geração de indicadores. O RailOps centraliza
essas informações em uma aplicação web com um núcleo comum e regras específicas
para cada terminal.

A documentação de requisitos, casos de uso, regras de negócio, arquitetura,
modelagem, protótipos e backlog está no repositório
[railops-docs](https://github.com/ChoqueanoIV/railops-docs).

## Funcionalidades disponíveis

- autenticação por matrícula e PIN, com primeiro acesso e token JWT;
- escolha entre Pátio Brisamar e Terminal TECON;
- registro da passagem de serviço do Brisamar;
- registro da passagem de serviço do TECON, incluindo atendimento condicional
  e dados independentes das Áreas 1 e 2;
- validações das regras de negócio no backend;
- persistência em PostgreSQL e migrations versionadas com Alembic;
- testes automatizados das camadas de schema, service, repository e rotas.

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Backend | Python, FastAPI e Pydantic |
| Persistência | PostgreSQL (Supabase), SQLAlchemy e Alembic |
| Frontend | HTML, CSS e JavaScript |
| Autenticação | JWT, Passlib e bcrypt |
| Testes | Pytest |
| Versionamento | Git e GitHub |

## Estrutura do repositório

```text
railops-app/
├── backend/
│   ├── alembic/            # migrations do banco de dados
│   ├── app/
│   │   ├── core/           # conexão e configuração do banco
│   │   ├── models/         # modelos SQLAlchemy
│   │   ├── repositories/   # acesso aos dados
│   │   ├── routers/        # endpoints da API
│   │   ├── schemas/        # contratos e validações Pydantic
│   │   └── services/       # regras de negócio
│   ├── tests/              # testes automatizados
│   ├── main.py             # inicialização da API FastAPI
│   └── requirements.txt
├── frontend/
│   ├── css/
│   ├── js/
│   └── *.html              # login, terminais e formulários
├── pytest.ini
└── README.md
```

## Como executar localmente

Pré-requisitos: Python 3 instalado e acesso a um banco PostgreSQL.

No PowerShell, a partir da raiz do repositório:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

Crie `backend/.env` com as variáveis abaixo. Não versione esse arquivo nem
publique os valores reais:

```dotenv
DATABASE_URL=postgresql://usuario:senha@host:porta/banco
JWT_SECRET_KEY=uma-chave-secreta-forte
```

Aplique as migrations:

```powershell
Set-Location backend
..\venv\Scripts\python.exe -m alembic upgrade head
Set-Location ..
```

Inicie a API:

```powershell
.\venv\Scripts\python.exe -m uvicorn main:app --reload --app-dir backend
```

Em outro terminal, inicie o frontend:

```powershell
.\venv\Scripts\python.exe -m http.server 3000 --directory frontend
```

Acesse `http://127.0.0.1:3000`. A documentação interativa da API fica em
`http://127.0.0.1:8000/docs`.

## Testes

```powershell
.\venv\Scripts\python.exe -m pytest
```

A suíte atual possui 48 testes automatizados.

## Roadmap

- [x] Requisitos, casos de uso e regras de negócio
- [x] Arquitetura, modelagem do banco e protótipos
- [x] Planejamento de branches e backlog
- [x] Autenticação e primeiro acesso
- [x] Passagem de serviço do Pátio Brisamar
- [x] Passagem de serviço do Terminal TECON
- [ ] Edição e histórico de passagens
- [ ] Consulta com filtros
- [ ] Exportação CSV e Excel
- [ ] Diagramas operacionais na aplicação
- [ ] Relatório de falhas por rádio
- [ ] Deploy e documentação final

## Autor

Desenvolvido por [Leandro](https://github.com/ChoqueanoIV) como projeto de
portfólio para transição de carreira em desenvolvimento de software.
