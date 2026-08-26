# Homologação operacional e de UX

Status: `EM ANDAMENTO`

## Objetivo

Validar o produto já implementado em um ambiente limpo, com pessoas
representativas do uso real, antes de criar novas funcionalidades.

## Escopo

- seguir o README para subir banco, API e frontend;
- validar primeiro acesso, login e logout;
- registrar uma passagem completa de Brisamar;
- registrar uma passagem completa de TECON, com e sem atendimento;
- consultar e editar uma passagem dentro da janela permitida;
- confirmar o comportamento somente leitura fora da janela de edição;
- avaliar clareza dos campos, mensagens, navegação e confirmação;
- registrar defeitos e dúvidas sem mudar regras durante a sessão;
- consolidar evidências e classificar achados por severidade.

## Fora do escopo

- implementar histórico, filtros, exportações ou relatórios;
- escolher ou executar deploy público;
- remover o frontend legado ou adaptadores;
- alterar janela de edição, identidade da passagem ou regras dos terminais;
- corrigir achados antes que sejam reproduzidos e classificados.

## Critérios de aceite

- [x] instalação reproduzida a partir do README em ambiente limpo;
- [ ] fluxos críticos executados e resultados registrados;
- [x] regras protegidas pelo baseline permanecem equivalentes;
- [x] problemas encontrados possuem passos de reprodução e severidade;
- [ ] decisões necessárias para a Task 020 estão documentadas;
- [x] checkpoint indica claramente o próximo passo aprovado.

## Evidências

Preencher ao executar a task:

- Branch: `test/homologacao-operacional`.
- Ambiente: Docker Desktop, PostgreSQL 17, backend containerizado e React/Vite
  local; migration no `head`.
- Participantes/perfis: homologação técnica automatizada pelo mantenedor;
  avaliação com usuários representativos ainda pendente.
- Fluxos aprovados: primeiro acesso, login, logout, proteção de rota, Brisamar,
  TECON sem atendimento, consulta, edição autorizada e modo somente leitura.
- Defeitos encontrados: handler de validação pode transformar `422` em `500`;
  severidade alta e reprodução em
  [`../validation/019-technical-homologation.md`](../validation/019-technical-homologation.md).
- Decisões de produto: gates da Task 020 ainda dependem dos usuários.
- Testes automatizados: backend 133 aprovados e 94% de cobertura; frontend 13
  aprovados; lint, formato, tipos e builds aprovados.
- Observações: nenhuma correção ou regra de negócio foi alterada nesta etapa.
