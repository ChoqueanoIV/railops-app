# RailOps

Sistema web de gestão de passagens de serviço para operação ferroviária,
desenvolvido para substituir o processo em papel utilizado no Pátio Brisamar
e no Terminal TECON.

> 🚧 **Status do projeto:** em desenvolvimento — Fase de Casos de Uso.
> Nenhuma versão implantada ainda.

---

## 📋 Sobre o projeto

Hoje, a passagem de serviço entre turnos é preenchida em papel, arquivada
fisicamente e sem possibilidade de busca, indicadores ou histórico
organizado. O RailOps digitaliza esse processo com um sistema web único,
capaz de atender múltiplos terminais (com um núcleo de dados comum e
seções específicas por terminal), preparado desde a arquitetura para
crescer sem retrabalho.

Este projeto nasceu como estudo de caso real de um operador ferroviário e
foi conduzido seguindo um processo de engenharia de software completo:
levantamento de requisitos, casos de uso, arquitetura, modelagem de banco,
protótipos, backlog e testes — antes de qualquer linha de código.

📄 A documentação completa do processo está no repositório irmão:
**[railops-docs](https://github.com/ChoqueanoIV/railops-docs)**

## 🧱 Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| Backend | Python + FastAPI |
| Banco de dados | PostgreSQL (Supabase) |
| Frontend | HTML, CSS, JavaScript (evolução futura para React) |
| Autenticação | Supabase Auth |
| Testes | Pytest |
| Deploy | Render (ou equivalente gratuito) |
| Versionamento | Git + GitHub |

## 📁 Estrutura do repositório

```
railops-app/
├── backend/        # API em FastAPI
├── frontend/        # Interface web
└── .github/
    └── workflows/    # Pipelines de CI/CD
```

## 🚀 Como rodar localmente

> Instruções detalhadas serão adicionadas a partir da Fase 9
> (Implementação).

## 🗺️ Roadmap

- [x] Levantamento de requisitos
- [ ] Casos de uso
- [ ] Arquitetura e modelagem do banco
- [ ] Protótipos de interface
- [ ] Implementação do backend
- [ ] Implementação do frontend
- [ ] Testes automatizados
- [ ] Deploy

## 📚 Documentação relacionada

- [railops-docs](https://github.com/ChoqueanoIV/railops-docs) — requisitos,
  casos de uso, arquitetura, ADRs e backlog.

## 👤 Autor

Desenvolvido por [Leandro] como projeto de portfólio para transição de
carreira em desenvolvimento de software.
