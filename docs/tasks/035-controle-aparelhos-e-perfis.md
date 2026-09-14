# Task 035 — Condição dos aparelhos e permissão de preenchimento

## Contexto operacional

O piloto precisa registrar como os aparelhos são entregues entre turnos e impedir que perfis de auditoria criem uma passagem. O celular da TECON pertence à passagem TECON; o celular do EOT e os Mobiles da sala da equipe pertencem à passagem Brisamar.

## Critérios de aceite

- A passagem Brisamar exige condição declarada do celular EOT, quantidade de Mobiles na sala (zero é válido) e condição declarada dos Mobiles.
- A passagem TECON exige condição declarada do celular TECON, mesmo quando não houve atendimento.
- Campos vazios são recusados na criação/edição; rascunhos anteriores sem os novos dados devem ser atualizados antes da confirmação. Passagens já confirmadas permanecem legíveis.
- Cada formulário orienta quais manobradores devem constar na equipe do terminal.
- Somente perfil `MANOBRADOR` pode criar, editar e confirmar. `INSTRUTOR` e `MONITOR_QUALIDADE` podem consultar, auditar e exportar conforme as permissões já existentes. A API impõe essa regra independentemente da interface.
- Dados novos aparecem na revisão e no PDF individual; a migração preserva registros anteriores.

## Evidências

- Backend: 194 testes passaram, incluindo validação dos novos campos, perfis e rascunhos anteriores.
- Frontend: 38 testes passaram; lint, type-check e build de produção passaram.
- O fluxo E2E foi atualizado, mas sua execução local depende do Docker Desktop, cujo daemon não estava disponível nesta sessão.

## Implantação

Aplicar `alembic upgrade head` antes de servir o novo backend (o script de início no Render já faz isso). A publicação deve seguir a ordem banco/backend e depois frontend. A atribuição real do perfil a matrículas de instrutores/monitores é administrativa; sem ela, novos usuários continuam com o perfil padrão `MANOBRADOR`.
