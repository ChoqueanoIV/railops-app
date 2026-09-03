from pathlib import Path

WORKFLOW = Path(__file__).parents[3] / ".github" / "workflows" / "quality.yml"


def test_ci_executa_em_pull_request_e_main_com_permissao_minima() -> None:
    conteudo = WORKFLOW.read_text(encoding="utf-8")

    assert "pull_request:" in conteudo
    assert "branches: [main]" in conteudo
    assert "contents: read" in conteudo
    assert "actions/checkout@" in conteudo


def test_ci_backend_usa_lock_banco_descartavel_e_gates_locais() -> None:
    conteudo = WORKFLOW.read_text(encoding="utf-8")

    assert "postgres:16-alpine" in conteudo
    assert "railops_test" in conteudo
    assert "uv sync --frozen" in conteudo
    assert "uv run --frozen ruff check ." in conteudo
    assert "uv run --frozen ruff format --check ." in conteudo
    assert "uv run --frozen mypy backend" in conteudo
    assert "uv run --frozen pytest --cov=backend/app" in conteudo
    assert "secrets." not in conteudo


def test_ci_frontend_usa_lock_e_todos_os_gates_locais() -> None:
    conteudo = WORKFLOW.read_text(encoding="utf-8")

    assert "working-directory: frontend/react" in conteudo
    assert "frontend/react/package-lock.json" in conteudo
    assert "run: npm ci" in conteudo
    assert "run: npm run format:check" in conteudo
    assert "run: npm run lint" in conteudo
    assert "run: npm run typecheck" in conteudo
    assert "run: npm test" in conteudo
    assert "run: npm run build" in conteudo


def test_ci_e2e_usa_docker_chromium_e_publica_somente_falhas() -> None:
    conteudo = WORKFLOW.read_text(encoding="utf-8")

    assert "name: E2E" in conteudo
    assert "npx playwright install --with-deps chromium" in conteudo
    assert "run: npm run test:e2e" in conteudo
    assert "if: failure()" in conteudo
    assert "actions/upload-artifact@v7" in conteudo
    assert "frontend/react/playwright-report" in conteudo
    assert "frontend/react/test-results" in conteudo
