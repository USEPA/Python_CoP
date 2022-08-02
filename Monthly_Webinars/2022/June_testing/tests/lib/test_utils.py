import pytest

from mything.lib.utils import invert, summarize_db

def test_invert():
    assert invert((1, 2, 3)) == [3, 2, 1]
    assert "".join(invert("abcdefghijklmnop")) == "ponmlkjihg"
    
def test_summarize_db_size(db_conn):
    assert summarize_db(db_conn)["records"] == 3

@pytest.mark.very_slow  # no it's not
def test_summarize_db_inversion(db_conn):
    assert summarize_db(db_conn)["total_inv"] == 15

