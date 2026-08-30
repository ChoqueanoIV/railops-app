# Descoberta e contrato de consulta

Status: `PLANEJADA`

## Objetivo

Definir e validar o contrato da futura consulta navegável de passagens sem
implementar listagem, filtros ou mudanças de persistência. A unidade exibida
deve ser o ciclo consolidado confirmado, preservando Brisamar e TECON como
partes da mesma passagem operacional.

## Dependência

- Task 019C integrada no PR #42;
- decisões do gate da Task 020 registradas em `docs/ROADMAP.md`.

## Comportamento existente caracterizado

- qualquer usuário autenticado pode consultar uma passagem pelo UUID;
- `GET /passagens/{passagem_id}` devolve o conteúdo completo de um terminal;
- `GET /passagens/ciclos/{ciclo_id}` devolve Brisamar e TECON consolidados;
- ciclos possuem identidade por data de início, turma e turno;
- ciclos confirmados possuem `confirmado_em` e são somente leitura;
- o responsável persiste como relacionamento com `Usuario`;
- ainda não existe endpoint de coleção, paginação ou filtros;
- `Usuario` não possui perfil ou cargo para distinguir Manobrador, Instrutor e
  Monitor de Qualidade;
- snapshots de edição existem, mas não possuem consulta HTTP ou interface.

## Decisões de contrato

- recurso da coleção: ciclos de passagem confirmados;
- rota proposta: `GET /passagens/ciclos`;
- autenticação: Bearer JWT obrigatória;
- acesso: todos os usuários autenticados cadastrados;
- ordenação fixa: `confirmado_em` decrescente, com `id` decrescente como
  desempate estável;
- período padrão: últimos 30 dias, considerando a data de início do turno;
- paginação padrão: página 1 com 20 ciclos;
- períodos maiores são permitidos e não provocam exclusão de registros;
- filtros opcionais combináveis: data inicial, data final, terminal, turma,
  turno, responsável e protocolo;
- protocolo corresponde ao UUID do ciclo consolidado;
- filtro de terminal seleciona ciclos que possuam a passagem daquele terminal,
  sem remover o outro terminal da resposta consolidada;
- responsável pode ser localizado por matrícula ou nome, com identificação
  inequívoca na resposta;
- somente ciclos em estado `CONFIRMADO` entram na coleção;
- o detalhe deve reutilizar o contrato consolidado já existente e permanecer
  somente leitura;
- a coleção expõe responsável, horário de confirmação e os dois terminais;
- rascunhos e snapshots não fazem parte deste endpoint.

## Contrato HTTP proposto

Parâmetros de query:

| Campo | Tipo | Padrão | Regra |
|---|---|---|---|
| `data_inicio` | data ISO | hoje menos 29 dias | data de início do turno |
| `data_fim` | data ISO | hoje | inclusiva e não anterior ao início |
| `terminal` | enum | ausente | `BRISAMAR` ou `TECON` |
| `turma` | enum | ausente | `A`, `B`, `C` ou `D` |
| `turno` | enum | ausente | `DIURNO` ou `NOTURNO` |
| `responsavel` | texto | ausente | matrícula exata ou trecho do nome |
| `protocolo` | UUID | ausente | identificador do ciclo |
| `pagina` | inteiro | `1` | mínimo 1 |
| `por_pagina` | inteiro | `20` | mínimo 1 e máximo 100 |

Resposta de sucesso proposta:

```json
{
  "itens": [
    {
      "id": "uuid-do-ciclo",
      "data": "2026-08-30",
      "turma": "C",
      "turno": "DIURNO",
      "estado": "CONFIRMADO",
      "confirmado_em": "2026-08-30T21:45:00Z",
      "responsavel": {
        "nome": "Nome cadastrado",
        "matricula": "12345678"
      },
      "passagens": []
    }
  ],
  "paginacao": {
    "pagina": 1,
    "por_pagina": 20,
    "total_itens": 1,
    "total_paginas": 1
  }
}
```

## Compatibilidade obrigatória

- não alterar os endpoints atuais de criação, edição, consulta ou confirmação;
- não mudar identidade, janela de turno ou regras internas dos terminais;
- não expor rascunhos na coleção pública;
- não modificar snapshots ou criar política de retenção;
- não adicionar perfil/cargo por inferência a partir de matrícula;
- manter registros legados consultáveis pelo endpoint individual, mesmo quando
  não puderem compor um ciclo consolidado.

## Fora de escopo

- implementar repository, service, controller ou tela de listagem;
- criar migration;
- definir a fonte oficial dos cargos de Instrutor e Monitor de Qualidade;
- consultar snapshots de edição;
- exportar CSV/PDF ou produzir relatórios;
- alterar autenticação ou claims do JWT.

## Critérios de aceite

- [ ] inventário atual confrontado com controller, schemas, models e testes;
- [ ] unidade de consulta definida como ciclo consolidado confirmado;
- [ ] filtros, ordenação, período e paginação definidos sem ambiguidade;
- [ ] resposta inclui protocolo, responsável e horário de confirmação;
- [ ] compatibilidade com os endpoints atuais explicitamente protegida;
- [ ] acesso a rascunhos e snapshots excluído deste contrato;
- [ ] ausência atual de perfil/cargo registrada como dependência futura;
- [ ] nenhum código funcional ou schema de banco alterado;
- [ ] plano da Task 021 pode ser derivado sem inventar regra de negócio.

## Evidências

A preencher durante a execução da task.
