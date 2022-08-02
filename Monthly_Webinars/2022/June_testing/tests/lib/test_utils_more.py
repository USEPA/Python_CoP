import pytest

from mything.lib.utils import invert

FLIPPED = [
    ([1, 2, 3], [3, 2, 1]),
    (['a', 'b', 'c'], ['c', 'b', 'a']),
    (["one", "two", "three"], ["three", "two", "one"]),
]

# parameters listed in FLIPPED
# `ids` is a list / iterable of human readable names for items
@pytest.mark.parametrize(("forward", "back"), FLIPPED, ids=[str(i[0]) for i in FLIPPED])
def test_more_invert(forward, back):
    assert invert(forward) == back

# parameters listed in FLIPPED
@pytest.mark.parametrize(("forward", "back"), FLIPPED)
@pytest.mark.extras  # test not run without --my-extras, see conftest.py
def test_more2_invert(forward, back):
    assert invert(forward) == back
