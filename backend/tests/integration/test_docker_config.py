from pathlib import Path

RAIZ_PROJETO = Path(__file__).resolve().parents[3]


def test_dockerfile_executa_backend_com_usuario_nao_root() -> None:
    dockerfile = (RAIZ_PROJETO / "backend" / "Dockerfile").read_text(encoding="utf-8")

    assert "USER railops" in dockerfile
    assert "app.main:app" in dockerfile
    assert "HEALTHCHECK" in dockerfile
    assert "/ready" in dockerfile
    assert "COPY backend/.env" not in dockerfile


def test_compose_exige_segredos_e_executa_migration_antes_da_api() -> None:
    compose = (RAIZ_PROJETO / "compose.yaml").read_text(encoding="utf-8")

    assert "POSTGRES_PASSWORD:?" in compose
    assert "JWT_SECRET_KEY:?" in compose
    assert "alembic upgrade head && exec uvicorn" in compose
    assert "condition: service_healthy" in compose
    assert "read_only: true" in compose
    assert "/ready" in compose


def test_contexto_docker_exclui_arquivos_sensiveis_e_testes() -> None:
    itens_ignorados = set(
        (RAIZ_PROJETO / ".dockerignore").read_text(encoding="utf-8").splitlines()
    )

    assert ".env" in itens_ignorados
    assert ".env.*" in itens_ignorados
    assert "backend/tests" in itens_ignorados
