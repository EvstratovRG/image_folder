from pathlib import Path

import pytest

DATA_PATH = Path(__file__).parent / "data"

pytest_plugins = []


@pytest.fixture(autouse=True)
def inject_db_session_into_middleware(db_test_session, mocker):
    mocker.patch("main.SessionLocal", side_effect=lambda: db_test_session)
