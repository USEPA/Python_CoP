"""Define fixtures and pytest config. here."""

import sqlite3

import pytest

@pytest.fixture(scope="session")
def db_conn(tmp_path_factory):
    """Dummy DB for testing"""
    # tmp_path_factory is a built in pytest fixture
    db_file = tmp_path_factory.mktemp("tmp_data") / "data.db"
    conn = sqlite3.connect(db_file)
    conn.execute("create table people (name text, role text)")
    conn.executemany(
        "insert into people values (?, ?)",
        [
            ["Jo", "Stats"],
            ["Ng", "Docs."],
            ["Samarasinghe", "DevOp"],
        ]
    )
    return conn


def pytest_addoption(parser):
    # Allow user to specify --my-extras parameter,
    # store are bool.
    parser.addoption(
        "--my-extras", action="store_true", help="run tests marked `extras`"
    )


def pytest_runtest_setup(item):
    # Don't run tests marked `extras` unless --my-extras passed
    # on command line.
    if "extras" in item.keywords and not item.config.getoption("--my-extras"):
        pytest.skip("need --my-extras option to run this test")
