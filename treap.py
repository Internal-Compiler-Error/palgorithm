"""
A treap: a binary search tree on keys that is also a heap on random priorities.

Conventions the tests rely on:
- Keys are unique; inserting a key that is already present changes nothing.
- Priorities form a min-heap: every node's priority is smaller than its
  children's, so the smallest priority sits at the root.
- select() and rank() are 1-based, like avl.py.

insert/delete can be written with rotations (like avl.py) or on top of
split/merge. Either passes the tests.
"""

import random
from collections.abc import Iterator

type Key = float


class Node:
    def __init__(self, key: Key, priority: float) -> None:
        self.key = key
        self.priority = priority
        self.left: Node | None = None
        self.right: Node | None = None
        # Number of nodes in this subtree. Tests only check it from stage 6 on.
        self.size = 1


class Treap:
    def __init__(self, rng: random.Random | None = None) -> None:
        self.root: Node | None = None
        # Tests pass a seeded Random so that "random" priorities are reproducible.
        self.rng = rng if rng is not None else random.Random()

    def insert(self, key: Key, priority: float | None = None) -> bool:
        """
        Add key. Returns False if it was already present.

        priority=None means draw one from self.rng. Tests pass explicit
        priorities to get an exact, predictable shape.
        """
        raise NotImplementedError

    def delete(self, key: Key) -> bool:
        """Remove key. Returns False if it was not present."""
        raise NotImplementedError

    def __contains__(self, key: Key) -> bool:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __iter__(self) -> Iterator[Key]:
        """Yield keys in ascending order."""
        raise NotImplementedError

    def min(self) -> Key:
        """Smallest key. ValueError if empty."""
        raise NotImplementedError

    def max(self) -> Key:
        """Largest key. ValueError if empty."""
        raise NotImplementedError

    def select(self, i: int) -> Key:
        """The i-th smallest key, 1-based. IndexError if i is out of range."""
        raise NotImplementedError

    def rank(self, key: Key) -> int:
        """1-based position of key in sorted order. KeyError if absent."""
        raise NotImplementedError


def split(t: Node | None, key: Key) -> tuple[Node | None, Node | None]:
    """
    Split t into (keys < key, keys >= key), both valid treaps.

    Consumes t: reuse its nodes rather than copying them.
    """
    raise NotImplementedError


def merge(a: Node | None, b: Node | None) -> Node | None:
    """
    Join two treaps into one, where every key in a is less than every key in b.

    Consumes a and b.
    """
    raise NotImplementedError
