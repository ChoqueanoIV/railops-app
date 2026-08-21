import os

import pytest


@pytest.fixture
def banco_teste_url() -> str:
    url = os.environ["DATABASE_URL"]
    assert os.environ["RAILOPS_ENV"] == "test"
    assert url.rsplit("/", maxsplit=1)[-1] == "railops_test"
    return url
