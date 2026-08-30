# Histórico auditável de edições

Status: `PLANEJADA`

## Objetivo

Permitir que Instrutores e Monitores de Qualidade consultem o histórico
auditável das alterações realizadas antes da confirmação final, preservando a
consulta do conteúdo confirmado para todos os usuários autenticados.

## Dependências

- Task 020 integrada no PR #43;
- Task 021 integrada no PR #44;
- gate de perfis e visibilidade aprovado em `docs/ROADMAP.md`.

## Baseline protegido

- matrícula, primeiro acesso, PIN, JWT e duração da sessão;
- consulta final disponível a qualquer usuário autenticado;
- edição restrita ao autor, à janela do turno e ao estado não confirmado;
- snapshot criado antes de cada edição na mesma transação da atualização;
- unicidade sequencial da versão por passagem;
- Brisamar e TECON consolidados no mesmo ciclo;
- passagens confirmadas permanecem somente leitura.

## Regras de negócio aprovadas

- perfis disponíveis: `MANOBRADOR`, `INSTRUTOR` e `MONITOR_QUALIDADE`;
- perfil pertence ao usuário cadastrado e não é deduzido da matrícula;
- usuários existentes recebem `MANOBRADOR`;
- somente `INSTRUTOR` e `MONITOR_QUALIDADE` acessam snapshots;
- `MANOBRADOR` continua acessando somente o conteúdo final confirmado;
- histórico mostra versão, data/hora, responsável pela alteração, estado
  anterior e conteúdo final;
- nenhuma credencial, hash, token ou código de ativação pode ser exposto;
- atribuição de perfil especial não faz parte da interface desta task.

## Escopo backend

- adicionar enum tipado de perfil ao domínio de autenticação;
- criar migration com `MANOBRADOR` como valor seguro para registros existentes;
- manter tokens atuais válidos, resolvendo o perfil pelo usuário carregado do
  banco, sem depender de claim nova;
- criar dependência reutilizável que autorize Instrutor ou Monitor de Qualidade;
- adicionar leitura paginada e ordenada dos snapshots de uma passagem;
- montar comparação entre cada snapshot anterior e o estado final confirmado;
- expor responsável pela alteração com nome e matrícula;
- devolver `403` padronizado para Manobradores e `404` para recurso inexistente;
- não devolver colunas internas, objetos ORM ou dados de autenticação;
- documentar um comando administrativo idempotente para atribuição explícita de
  perfil por matrícula em ambiente controlado.

## Contrato HTTP proposto

- `GET /passagens/{passagem_id}/historico`;
- autenticação Bearer obrigatória;
- autorização restrita a `INSTRUTOR` e `MONITOR_QUALIDADE`;
- paginação por `pagina` e `por_pagina`, com 20 itens por padrão e máximo 100;
- ordenação por versão decrescente;
- resposta com identificação da passagem, conteúdo final e versões históricas;
- cada versão contém número, `alterado_em`, responsável e snapshot anterior;
- coleção vazia é válida quando a passagem nunca foi editada.

## Escopo frontend

- disponibilizar “Ver histórico de alterações” no detalhe confirmado somente
  quando a API autorizar;
- criar tela protegida de histórico com resumo da passagem e versões;
- comparar campos anteriores e finais de forma legível por seção;
- destacar valores alterados sem ocultar campos não modificados;
- mostrar responsável e horário de cada versão;
- oferecer paginação, estados vazio, carregamento e erro;
- tratar `403` sem encerrar uma sessão autenticada válida;
- manter o detalhe final e a listagem da Task 021 inalterados.

## Migração e compatibilidade

- migration deve possuir upgrade e downgrade tecnicamente seguro;
- downgrade só pode remover o perfil após converter valores especiais para
  `MANOBRADOR`, sem excluir usuários;
- nenhuma matrícula, PIN ou passagem pode ser modificada pela migration;
- autenticação de usuários existentes deve continuar funcionando;
- snapshots históricos atuais devem permanecer válidos e consultáveis;
- não reescrever snapshots anteriores para simular dados inexistentes.

## Testes obrigatórios

### Backend

- migration upgrade/downgrade/re-upgrade preservando usuários;
- autenticação existente com perfil padrão;
- autorização para cada um dos três perfis;
- resposta 403 sem vazamento para Manobrador;
- histórico vazio, paginação, ordenação e passagem inexistente;
- responsável e snapshot serializados sem credenciais;
- compatibilidade dos endpoints existentes.

### Frontend

- acesso autorizado e bloqueado;
- histórico vazio e com múltiplas versões;
- responsável, data/hora e diferenças visíveis;
- paginação e tratamento de erro;
- detalhe confirmado continua somente leitura.

## Fora de escopo

- tela administrativa de usuários ou perfis;
- cadastro autônomo de usuários;
- alteração ou exclusão de snapshots;
- exportação, impressão, CSV, PDF ou relatório consolidado;
- retenção ou descarte automático do histórico;
- edição posterior à confirmação;
- alteração das regras internas dos terminais.

## Critérios de aceite

- [ ] perfis explícitos persistidos com padrão seguro para usuários existentes;
- [ ] login e tokens atuais permanecem compatíveis;
- [ ] somente Instrutor e Monitor acessam snapshots;
- [ ] Manobrador recebe 403 e mantém acesso ao conteúdo final;
- [ ] histórico mostra versão, horário, responsável, anterior e final;
- [ ] dados de autenticação nunca aparecem no contrato;
- [ ] snapshots existentes permanecem intactos;
- [ ] migration validada nos dois sentidos sem perda de usuários;
- [ ] procedimento administrativo de atribuição documentado;
- [ ] backend, frontend, Docker e CI aprovados;
- [ ] nenhuma regra operacional não autorizada é alterada.

## Evidências

A preencher durante a execução da task.
