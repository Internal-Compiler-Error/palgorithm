# pyright: reportOptionalMemberAccess=false
import random
from math import ceil, floor

from avl import Root


def test_single_node(t: Root):
    t.insert(5)
    assert t.left.key == 5

def test_insert_sorted(t: Root):
    t.insert(1)
    assert t.left.key == 1

    t.insert(2)
    assert t.left.key == 1

    t.insert(3)

    root = t.left
    assert root.key == 2
    assert root.left.key == 1
    assert root.right.key == 3


def test_insert_reversed(t: Root):
    t.insert(3)
    t.insert(2)
    t.insert(1)

    t.traverse()

def test_delete_stuff(t: Root):
    t.insert(3)
    t.insert(2)
    t.insert(1)

    t.delete(2)
    t.traverse()

def test_delete_stuffv2(t: Root):
    for i in range(30):
        t.insert(i)

    to_delete = [5, 1, 26, 9, 28, 19, 27, 3, 18, 24, 15, 10, 23, 16, 13, 11, 12, 2, 14, 8, 29, 6, 25, 0, 4, 17, 22, 21, 20, 7]

    for e in to_delete:
        try:
            t.delete(e)
        except AssertionError:
            print(f"failed on ={e} in {to_delete}")
            raise


    t.traverse()

def test_delete_stuff_extreme(t: Root):
    n = 1000
    for i in range(n):
        t.insert(i)

    t.traverse()

    import random
    to_delete = list(range(n))
    random.shuffle(to_delete)

    for i in to_delete:
        t.delete(i)
        t.traverse()

    t.traverse()
def test_delete_root(t: Root):
    for i in range(100):
        t.insert(i)

    for i in range(100):
        t.delete(t.left.key)
    t.traverse()

def test_insert_many(t: Root):
    l = list(range(100))
    random.shuffle(l)

    for i in l:
        t.insert(i)


def test_find_median(t: Root):
    t.insert(-1)
    t.insert(-2)
    t.insert(-3)
    t.insert(-4)
    n = t.left.size
    print(t.left.size)
    upper_median = ceil((n + 1) / 2)
    lower_median = floor((n + 1) / 2)
    print(f"{upper_median=}, {lower_median=}")
