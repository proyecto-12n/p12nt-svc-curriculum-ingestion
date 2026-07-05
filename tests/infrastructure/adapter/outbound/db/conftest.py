from unittest.mock import MagicMock

import pytest


@pytest.fixture(name="session")
def session_fixture():
    return MagicMock()


def configure_first_result(session, value):
    session.exec.return_value.first.return_value = value


def configure_all_result(session, values):
    session.exec.return_value.all.return_value = values
