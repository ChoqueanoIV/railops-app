# Task 033 — Identidade visual Passagem de Turno Digital

## Objetivo

Adotar **Passagem de Turno Digital** como nome público do piloto e aproximar a
interface do contexto visual da MRS com azul, amarelo e branco, sem empregar
logotipo oficial nem alterar o nome técnico interno RailOps.

## Escopo

- tema claro, profissional e responsivo;
- identificação permanente do produto e do ambiente piloto;
- hierarquia visual operacional em login, seleção, formulários, consultas e revisão;
- orientação pelas etapas do formulário;
- manutenção integral dos campos, validações, payloads e regras existentes.

## Fora do escopo

- alteração de API, banco ou regra de negócio;
- uso do logotipo oficial da MRS sem autorização e manual de marca;
- transformação do formulário em fluxo paginado;
- mudança dos critérios de confirmação da passagem.

## Critérios de aceite

- o nome público exibido é “Passagem de Turno Digital”;
- o ambiente é identificado como piloto;
- azul, amarelo e branco estruturam a identidade visual com contraste adequado;
- o formulário apresenta acesso às suas etapas sem ocultar conteúdo;
- computador e celular permanecem funcionais;
- testes, lint, tipagem, formatação e build do frontend passam.

## Baseline

Executada em 10/09/2026 antes das alterações:

- Vitest: 34 testes aprovados;
- ESLint: aprovado;
- TypeScript: aprovado;
- Prettier: aprovado;
- build Vite: aprovado.

## Evidências finais

Executadas em 10/09/2026:

- Vitest: 34 testes aprovados;
- ESLint: aprovado;
- TypeScript: aprovado;
- build Vite: aprovado;
- inspeção visual da tela de login em navegador local: aprovada;
- contratos, payloads, API e banco: não alterados.
- testes E2E atualizados para os novos textos públicos, sem mudança de fluxo.

O teste de componente do formulário também confirma a presença da navegação
pelas etapas. A checagem de formatação foi repetida após o último ajuste.
