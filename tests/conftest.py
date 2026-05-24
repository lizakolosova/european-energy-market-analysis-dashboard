import sqlite3
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "data" / "energy.db"


@pytest.fixture(scope="module")
def db():
    assert DB_PATH.exists(), (
        f"Database not found at {DB_PATH}. Run `python src/load_data.py` first."
    )
    conn = sqlite3.connect(str(DB_PATH))
    yield conn
    conn.close()
