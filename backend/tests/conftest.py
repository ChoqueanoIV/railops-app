import os

import pytest

pytest_plugins = (
    "tests.fixtures.application",
    "tests.fixtures.database",
)

# O bootstrap dos testes não depende do .env nem de credenciais reais.
os.environ["DATABASE_URL"] = (
    "postgresql://railops_test:railops_test@localhost/railops_test"
)
os.environ["JWT_SECRET_KEY"] = "segredo-ficticio-exclusivo-para-testes"
os.environ["RAILOPS_ENV"] = "test"


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        caminho = item.path.as_posix()
        for marcador in ("unit", "integration", "api"):
            if f"/tests/{marcador}/" in caminho:
                item.add_marker(getattr(pytest.mark, marcador))
                break
