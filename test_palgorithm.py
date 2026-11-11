import pytest

from palgorithm import cyclic_shift_right, remove, set_intersection, set_union, unique


@pytest.mark.parametrize("arr, v, expected", [
    ([1, 2, 3], 1, [2, 3]),
    ([1, 1, 1], 1, []),
    ([1, 2, 3, 4, 5], 3, [1, 2, 4, 5]),
    ([1, 2, 3, 4, 5], 6, [1, 2, 3, 4, 5]),
    ([], 1, []),
    ([1], 1, []),
    ([1, 2, 1, 3, 1], 1, [2, 3]),
    ([5, 4, 3, 2, 1], 5, [4, 3, 2, 1]),
    ([1, 2, 3, 4, 5], 5, [1, 2, 3, 4]),
])
def test_remove(arr, v, expected):
    end = remove(arr, v)
    assert arr[:end] == expected


@pytest.mark.parametrize("arr, expected", [
    ([1, 1, 2, 2, 3, 3], [1, 2, 3]),
    ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
    ([1, 1, 1, 1, 1], [1]),
    ([], []),
    ([1], [1]),
    ([1, 1], [1]),
    ([1, 2, 2, 3, 3, 3, 4, 5, 5], [1, 2, 3, 4, 5]),
    ([0, 0, 0, 1, 1, 2, 3, 3, 3, 3, 4, 5, 5, 5], [0, 1, 2, 3, 4, 5]),
])
def test_unique(arr, expected):
    end = unique(arr)
    assert arr[:end] == expected


@pytest.mark.parametrize("x, y, expected", [
    ([1, 2, 3], [4, 5, 6], [1, 2, 3, 4, 5, 6]),
    ([1, 3, 5], [2, 3, 4, 5], [1, 2, 3, 4, 5]),
    ([], [1, 2, 3], [1, 2, 3]),
    ([1, 2, 3], [], [1, 2, 3]),
    ([], [], []),
    ([1, 1, 2, 3], [2, 3, 3, 4], [1, 1, 2, 3, 3, 4]),
    ([5, 6], [1, 2, 3], [1, 2, 3, 5, 6]),
    ([1, 2, 5, 7, 8, 10], [2, 3, 6, 8, 9, 11], [1, 2, 3, 5, 6, 7, 8, 9, 10, 11]),
    ([1, 2, 3], [1, 2, 3], [1, 2, 3]),
    ([-3, -1, 0, 2], [-2, -1, 0, 1], [-3, -2, -1, 0, 1, 2]),
])
def test_set_union(x, y, expected):
    out = []
    end = set_union(x, y, out)
    assert out[:end] == expected


@pytest.mark.parametrize("x, y, expected", [
    ([2, 3, 4, 5, 6, 7, 7, 8], [5, 7, 7, 9], [5, 7, 7]),
])
def test_set_intersection(x, y, expected):
    out = []
    end = set_intersection(x, y, out)
    assert out[:end] == expected


@pytest.mark.parametrize("arr, k, expected", [
    ([1, 2, 3, 4, 5], 2, [4, 5, 1, 2, 3]),
])
def test_cyclic_shift_right(arr, k, expected):
    cyclic_shift_right(arr, k)
    assert arr == expected
