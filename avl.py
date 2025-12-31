from __future__ import annotations

import turtle
from typing import Tuple


class Root:
    def __init__(self):
        self.left = None
        self.right = None
        self.parent = None

    def traverse(self):
        traverse(self.left)

class Node:
    def __init__(self, parent: Node | Root, key):
        self.left: Node | None = None
        self.right: Node | None = None
        self.parent: Node | Root = parent

        self.key = key
        self.height = 1


"""
                   y
              x       C
           A     B
into:
                   x
                A       y
                     B     C
"""
def rot_right(tree: Node):
    y = tree
    tree_parent = y.parent
    x = y.left
    a = x.left
    b = x.right
    c = y.right

    if tree_parent.left == y:
        tree_parent.left = x
    else:
        tree_parent.right = x

    y.parent = x
    x.parent = tree_parent

    x.left = a
    if a:
        a.parent = x

    x.right = y
    y.parent = x

    y.left = b
    if b:
        b.parent = y

    y.right = c
    if c:
        c.parent = y


    update_height(y)
    update_height(x)


"""
                   x
                A       y
                     B     C
into:
                   y
              x       C
           A     B

"""
def rot_left(tree: Node):
    x = tree
    y = x.right
    a = x.left
    b = y.left
    c = y.right

    tree_parent = x.parent
    if tree_parent.left == x:
        tree_parent.left = y
    else:
        tree_parent.right = y

    x.parent = y
    y.parent = tree_parent

    y.left = x

    y.right = c
    if c:
        c.parent = y

    x.left = a
    if a:
        a.parent = x

    x.right = b
    if b:
        b.parent = x

    update_height(x)
    update_height(y)


"""
Insert a new node at the tree rooted at t
"""
def insert(t: Root, key):
    if t.left == t.right is None:
        x = Node(t, key)
        t.left = x
        t.right = x
        return

    parent = t
    t = t.left
    while t is not None:
        parent = t
        if t.key <= key:
            t = t.right
        else:  # t.key > key:
            t = t.left

    x = Node(parent, key)

    if parent.key <= key:
        parent.right = x
    else: # t.key > key:
        parent.left = x

    fixup_tree(x.parent)

def delete(t: Root, key):
    root = t

    parent = None
    t = t.left
    while t:
        parent = t
        if t.key < key:
            t = t.right
        elif t.key > key:
            t = t.left
        else: # t.key == key
            break

    if t is None: return None # key doesn't exist
    if parent is None: return None # deleting the root node

    if t.left is None:
        transplant(root, t, t.right)
        fixup_tree(t.parent)
        return None
    elif t.right is None:
        transplant(root, t, t.left)
        fixup_tree(t.parent)
        return None
    else: # both children are present
        # find t's successor
        y = t.right
        while y.left is not None:
            y = y.left

        if y != t.right:
            transplant(root, y, y.right)
            y.right = t.right
            y.right.parent = y

        transplant(root, t, y)
        y.left = t.left
        y.left.parent = y

        if y.right is not None:
            fixup_tree(y.right)
        else:
            fixup_tree(y)
        return None


def skew(t: Node) -> int:
    if t is None:
        return 0

    match t.left, t.right:
        case None, None: return 0
        case left, None: return -left.height
        case None, right: return right.height
        case left, right: return right.height - left.height

"""
Assuming subtree t violates the height balance property, fixup the invariants using rotates
"""
def fixup_subtree(t: Node):
    x = t
    skew_metric = skew(x)
    assert skew_metric in [-2, 2]
    if skew_metric == 2:
        z = x.right
        z_skew = skew(z)
        assert z_skew in [-1, 0, 1]

        match z_skew:
            case -1: rot_right(z); rot_left(x)
            case  0: rot_left(x)
            case  1: rot_left(x)
    else: # skew_metric == -2
        z = x.left
        z_skew = skew(z)
        assert z_skew in [-1, 0, 1]
        match z_skew:
            case -1: rot_right(x)
            case  0: rot_right(x)
            case  1: rot_left(z); rot_right(x)

"""
Replaces the subtree rooted at u with the one rooted at v
"""
def transplant(t: Root, u: Node, v: Node | None):
    if u.left == u.right:
        t.left = v
        t.right = v
    elif u == u.parent.left:
        u.parent.left = v
    else: # u == u.parent.right:
        u.parent.right = v

    if v is not None:
        v.parent = u.parent


"""
Assuming all levels below tree t are height balanced, fix any invariants that t might have, and all of t's parent tree.
"""
def fixup_tree(t: Node | Root):
    update_height(t)
    skew_metric = skew(t)

    if skew_metric not in [-1, 0, 1]:
        fixup_subtree(t)

    if t.left != t.right: # stop at root node
        fixup_tree(t.parent)


def update_height(t: Node | None):
    left = t.left.height if t.left else 0
    right = t.right.height if t.right else 0

    t.height = 1 + max(left, right)

#################### TESTS  #########################
def test_single_node():
    t = Root()
    insert(t, 5)
    assert t.left.key == 5

def test_insert_sorted():
    t = Root()
    insert(t, 1)
    assert t.left.key == 1

    insert(t, 2)
    assert t.left.key == 1

    insert(t,  3)

    t = t.left
    assert t.key == 2
    assert t.left.key == 1
    assert t.right.key == 3

def traverse(t: Node):
    if t is None:
        return

    traverse(t.left)
    print(t.key)
    traverse(t.right)

def test_insert_reversed():
    t = Root()
    insert(t, 3)
    insert(t, 2)
    insert(t, 1)

    t.traverse()

def test_delete_stuff():
    t = Root()
    insert(t, 3)
    insert(t, 2)
    insert(t, 1)

    delete(t, 3)
    t.traverse()



if __name__ == "__main__":
    pass




