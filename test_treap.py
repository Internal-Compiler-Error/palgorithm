# pyright: reportOptionalMemberAccess=false
"""
Tests for treap.py, ordered as a learning path:

    1. empty treap
    2. insert, search, iteration (plain BST part)
    3. heap order on priorities (the "treap" part)
    4. delete
    5. split and merge
    6. order statistics: size, select, rank
    7. randomized comparison against a Python set

Run with `uv run pytest test_treap.py -x`. -x stops at the first failure,
which is the next thing to implement.
"""

import math
import random
from collections.abc import Iterable

import pytest

from treap import Key, Node, Treap, merge, split

type Shape = tuple[Key, Shape, Shape] | None


# ---------------------------------------------------------------- helpers


def shape(n: Node | None) -> Shape:
    """The tree as nested (key, left, right) tuples, easy to compare and print."""
    if n is None:
        return None
    return (n.key, shape(n.left), shape(n.right))


def keys(n: Node | None) -> list[Key]:
    if n is None:
        return []
    return keys(n.left) + [n.key] + keys(n.right)


def height(n: Node | None) -> int:
    if n is None:
        return 0
    return 1 + max(height(n.left), height(n.right))


def check_invariants(n: Node | None, check_size: bool = False) -> None:
    """BST order on keys, min-heap order on priorities, and optionally sizes."""

    def go(n: Node | None, lo: Key | None, hi: Key | None) -> int:
        if n is None:
            return 0
        assert lo is None or lo < n.key, f"BST order broken at key {n.key}"
        assert hi is None or n.key < hi, f"BST order broken at key {n.key}"
        for child in (n.left, n.right):
            if child is not None:
                assert n.priority <= child.priority, (
                    f"heap order broken: {n.key} (priority {n.priority}) is above "
                    f"{child.key} (priority {child.priority})"
                )
        size = 1 + go(n.left, lo, n.key) + go(n.right, n.key, hi)
        if check_size:
            assert n.size == size, f"size of {n.key} is {n.size}, expected {size}"
        return size

    go(n, None, None)


def build(pairs: Iterable[tuple[Key, float]]) -> Treap:
    t = Treap()
    for k, p in pairs:
        t.insert(k, p)
    return t


def expected_shape(pairs: Iterable[tuple[Key, float]]) -> Shape:
    """
    With distinct keys and priorities, there is exactly one valid treap, and it
    is the plain (unbalanced) BST you get by inserting keys in priority order.
    """

    def bst_insert(s: Shape, k: Key) -> Shape:
        if s is None:
            return (k, None, None)
        key, left, right = s
        if k < key:
            return (key, bst_insert(left, k), right)
        return (key, left, bst_insert(right, k))

    s: Shape = None
    for k, _ in sorted(pairs, key=lambda kp: kp[1]):
        s = bst_insert(s, k)
    return s


def random_pairs(n: int, seed: int) -> list[tuple[Key, float]]:
    rng = random.Random(seed)
    ks = rng.sample(range(10 * n), n)
    return [(k, rng.random()) for k in ks]


# Hand-checked example. Sorted by priority the keys are 4, 3, 7, 5, 1, 8, so:
#
#            4
#          /   \
#         3     7
#        /     / \
#       1     5   8
#
SMALL = [(5, 0.5), (3, 0.2), (8, 0.9), (1, 0.7), (4, 0.1), (7, 0.3)]
SMALL_SHAPE = (4, (3, (1, None, None), None), (7, (5, None, None), (8, None, None)))


# ---------------------------------------------------------------- 1. empty treap


def test_empty():
    t = Treap()
    assert t.root is None
    assert len(t) == 0
    assert 1 not in t
    assert list(t) == []


def test_min_max_of_empty_raise():
    t = Treap()
    with pytest.raises(ValueError):
        t.min()
    with pytest.raises(ValueError):
        t.max()


# ---------------------------------------------------------------- 2. insert and search


def test_insert_one():
    t = Treap()
    assert t.insert(5) is True
    assert t.root.key == 5
    assert 5 in t
    assert len(t) == 1


def test_insert_duplicate_is_noop():
    t = Treap()
    t.insert(5)
    assert t.insert(5) is False
    assert len(t) == 1
    assert list(t) == [5]


def test_contains():
    t = Treap()
    for k in [10, 5, 15, 3, 7]:
        t.insert(k)
    for k in [10, 5, 15, 3, 7]:
        assert k in t
    for k in [0, 4, 6, 11, 100]:
        assert k not in t


def test_iter_is_sorted():
    ks = list(range(50))
    random.Random(1).shuffle(ks)
    t = Treap()
    for k in ks:
        t.insert(k)
    assert list(t) == list(range(50))
    assert len(t) == 50


def test_min_max():
    t = Treap()
    for k in [10, 5, 15, 3, 7]:
        t.insert(k)
    assert t.min() == 3
    assert t.max() == 15


# ---------------------------------------------------------------- 3. heap order


def test_smaller_priority_moves_up_left_child():
    t = Treap()
    t.insert(2, 0.5)
    t.insert(1, 0.1)
    assert shape(t.root) == (1, None, (2, None, None))


def test_smaller_priority_moves_up_right_child():
    t = Treap()
    t.insert(1, 0.5)
    t.insert(2, 0.1)
    assert shape(t.root) == (2, (1, None, None), None)


def test_new_node_rises_several_levels():
    t = build([(1, 0.3), (2, 0.4), (3, 0.5), (4, 0.6), (5, 0.0)])
    assert t.root.key == 5
    check_invariants(t.root)


def test_small_example_shape():
    t = build(SMALL)
    assert shape(t.root) == SMALL_SHAPE


def test_shape_does_not_depend_on_insertion_order():
    rng = random.Random(2)
    for _ in range(20):
        pairs = SMALL[:]
        rng.shuffle(pairs)
        assert shape(build(pairs).root) == SMALL_SHAPE


def test_shape_matches_priority_order_bst():
    pairs = random_pairs(200, seed=3)
    assert shape(build(pairs).root) == expected_shape(pairs)


def test_invariants_with_random_priorities():
    t = Treap(rng=random.Random(4))
    ks = list(range(500))
    random.Random(5).shuffle(ks)
    for k in ks:
        t.insert(k)
        check_invariants(t.root)


def test_same_seed_same_tree():
    a = Treap(rng=random.Random(6))
    b = Treap(rng=random.Random(6))
    for k in range(100):
        a.insert(k)
        b.insert(k)
    assert shape(a.root) == shape(b.root)


def test_sorted_inserts_stay_shallow():
    """A plain BST would turn this into a 2000-node linked list."""
    n = 2000
    t = Treap(rng=random.Random(7))
    for k in range(n):
        t.insert(k)
    assert height(t.root) <= 4 * math.log2(n)


# ---------------------------------------------------------------- 4. delete


def test_delete_from_empty():
    t = Treap()
    assert t.delete(1) is False


def test_delete_missing_key():
    t = build(SMALL)
    assert t.delete(6) is False
    assert shape(t.root) == SMALL_SHAPE


def test_delete_only_node():
    t = Treap()
    t.insert(1)
    assert t.delete(1) is True
    assert t.root is None
    assert len(t) == 0


def test_delete_leaf():
    t = build(SMALL)
    assert t.delete(8) is True
    assert shape(t.root) == (4, (3, (1, None, None), None), (7, (5, None, None), None))


def test_delete_node_with_one_child():
    t = build(SMALL)
    t.delete(3)
    assert shape(t.root) == (4, (1, None, None), (7, (5, None, None), (8, None, None)))


def test_delete_root_with_two_children():
    t = build(SMALL)
    t.delete(4)
    remaining = [(k, p) for k, p in SMALL if k != 4]
    assert shape(t.root) == expected_shape(remaining)


def test_delete_updates_len_and_contains():
    t = build(SMALL)
    t.delete(7)
    assert len(t) == len(SMALL) - 1
    assert 7 not in t
    assert list(t) == [1, 3, 4, 5, 8]


def test_delete_shape_matches_rebuild():
    pairs = random_pairs(200, seed=8)
    t = build(pairs)
    rng = random.Random(9)
    gone = set(rng.sample([k for k, _ in pairs], 100))
    for k in gone:
        assert t.delete(k) is True
    remaining = [(k, p) for k, p in pairs if k not in gone]
    assert shape(t.root) == expected_shape(remaining)


def test_delete_everything():
    t = Treap(rng=random.Random(10))
    ks = list(range(300))
    for k in ks:
        t.insert(k)
    random.Random(11).shuffle(ks)
    for k in ks:
        assert t.delete(k) is True
        check_invariants(t.root)
    assert t.root is None
    assert len(t) == 0


# ---------------------------------------------------------------- 5. split and merge


def test_split_empty():
    assert split(None, 5) == (None, None)


def test_split_at_present_key():
    t = build(random_pairs(100, seed=12))
    everything = list(t)
    pivot = everything[40]
    left, right = split(t.root, pivot)
    assert keys(left) == everything[:40]
    assert keys(right) == everything[40:]
    check_invariants(left)
    check_invariants(right)


def test_split_at_absent_key():
    t = build([(k, p) for k, p in random_pairs(50, seed=13)])
    everything = list(t)
    pivot = everything[20] + 0.5
    left, right = split(t.root, pivot)
    assert keys(left) == everything[:21]
    assert keys(right) == everything[21:]


def test_split_below_min_and_above_max():
    t = build(SMALL)
    left, right = split(t.root, 0)
    assert left is None
    assert shape(right) == SMALL_SHAPE

    t = build(SMALL)
    left, right = split(t.root, 100)
    assert shape(left) == SMALL_SHAPE
    assert right is None


def test_merge_with_empty():
    t = build(SMALL)
    assert shape(merge(t.root, None)) == SMALL_SHAPE
    t = build(SMALL)
    assert shape(merge(None, t.root)) == SMALL_SHAPE
    assert merge(None, None) is None


def test_merge_two_treaps():
    small = build([(1, 0.6), (2, 0.2), (3, 0.9)])
    big = build([(10, 0.4), (11, 0.1), (12, 0.5)])
    merged = merge(small.root, big.root)
    assert keys(merged) == [1, 2, 3, 10, 11, 12]
    check_invariants(merged)
    assert merged.key == 11


def test_merge_undoes_split():
    pairs = random_pairs(60, seed=14)
    original = shape(build(pairs).root)
    for pivot in sorted(k for k, _ in pairs):
        t = build(pairs)
        assert shape(merge(*split(t.root, pivot))) == original


# ---------------------------------------------------------------- 6. order statistics


def test_sizes_after_inserts():
    t = Treap(rng=random.Random(15))
    for k in random.Random(16).sample(range(1000), 200):
        t.insert(k)
        check_invariants(t.root, check_size=True)


def test_sizes_after_deletes():
    t = build(random_pairs(200, seed=17))
    for k in list(t)[::2]:
        t.delete(k)
        check_invariants(t.root, check_size=True)


def test_sizes_after_split_and_merge():
    t = build(random_pairs(100, seed=18))
    left, right = split(t.root, list(t)[30])
    check_invariants(left, check_size=True)
    check_invariants(right, check_size=True)
    check_invariants(merge(left, right), check_size=True)


def test_select():
    t = build(SMALL)
    assert [t.select(i) for i in range(1, 7)] == [1, 3, 4, 5, 7, 8]


def test_select_out_of_range():
    t = build(SMALL)
    with pytest.raises(IndexError):
        t.select(0)
    with pytest.raises(IndexError):
        t.select(7)
    with pytest.raises(IndexError):
        Treap().select(1)


def test_rank():
    t = build(SMALL)
    assert [t.rank(k) for k in [1, 3, 4, 5, 7, 8]] == [1, 2, 3, 4, 5, 6]


def test_rank_of_missing_key():
    t = build(SMALL)
    with pytest.raises(KeyError):
        t.rank(6)


def test_select_and_rank_are_inverses():
    t = build(random_pairs(300, seed=19))
    for i in range(1, len(t) + 1):
        assert t.rank(t.select(i)) == i


# ---------------------------------------------------------------- 7. randomized


def test_random_operations_match_a_set():
    rng = random.Random(20)
    t = Treap(rng=random.Random(21))
    model: set[int] = set()
    for step in range(3000):
        k = rng.randrange(200)
        if rng.random() < 0.6:
            assert t.insert(k) == (k not in model)
            model.add(k)
        else:
            assert t.delete(k) == (k in model)
            model.discard(k)

        assert len(t) == len(model)
        assert (k in t) == (k in model)
        if step % 50 == 0:
            assert list(t) == sorted(model)
            check_invariants(t.root, check_size=True)
            if model:
                ordered = sorted(model)
                i = rng.randrange(len(ordered))
                assert t.select(i + 1) == ordered[i]
                assert t.rank(ordered[i]) == i + 1
