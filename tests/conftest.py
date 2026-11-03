import pytest

import settings as app_settings
from modulos.aluno import Aluno


@pytest.fixture
def settings():
    return app_settings


@pytest.fixture
def aluno_fixture():
    return Aluno("2025001", "Maria", "maria@email.com")
