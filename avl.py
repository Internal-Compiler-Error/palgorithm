from math import ceil, floor
import random
from typing import List


class Root:
    def __init__(self):
        self.child = None
        self.parent = self

    def traverse(self):
        l = []
        traverse(self.left, l)
        assert l == sorted(l)

    @property
    def left(self):
        return self.child

    @left.setter
    def left(self, value):
        self.child = value

    @property
    def right(self):
        return self.child

    @right.setter
    def right(self, value):
        self.child = value

    def select(self, nth):
        t = self.child
        return select(t, nth)

    """
    Insert a new node at the tree rooted at t
    """
    def insert(self, key):
        t = self
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

    def delete(self, key):
        z = self
        parent = None
        z = z.left
        while z:
            parent = z
            if z.key < key:
                z = z.right
            elif z.key > key:
                z = z.left
            else: # z.key == key
                break

        if z is None: return None # key doesn't exist
        if parent is None: return None # deleting the root node

        if z.left is None:
            transplant(z, z.right)
            fixup_tree(parent)
            return None
        elif z.right is None:
            transplant(z, z.left)
            fixup_tree(parent)
            return None
        else: # both children are present
            # find z's successor
            y = z.right
            while y.left is not None:
                y = y.left

            old_parent = y.parent
            if y != z.right:
                transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            transplant(z, y)
            y.left = z.left
            y.left.parent = y

            if old_parent == z:
                fixup_tree(y)
            else:
                self.debug_tree("debug/what.png")
                fixup_tree(old_parent)
            return None

    def median(self):
        n = self.left.size

        upper = ceil((n + 1) / 2)
        lower = floor((n + 1) / 2)

        return (self.select(upper) + self.select(lower)) / 2

    def debug_tree(self, name="debug/tree.png"):
        t = debug_tree(self.left)

        if t is None:
            return
        import anytree.exporter
        anytree.exporter.UniqueDotExporter(t).to_picture(name)

class Node:
    def __init__(self, parent: "Node | Root", key):
        self.left: Node | None = None
        self.right: Node | None = None
        self.parent: Node | Root = parent

        self.key = key
        self.height = 1

        # augmented zone
        self.size = 1

    def rank(self):
        r = 1 + self.left.size if self.left else 1
        y = self

        # loop until we reach root
        while y.parent != y:
            if y.parent.right == y:
                r += y.parent.left.size if y.parent.left else 0
            y = y.parent

        return r


def traverse(t: Node, sink: List):
    if t is None:
        return

    traverse(t.left, sink)
    sink.append(t.key)
    traverse(t.right, sink)

def debug_tree(t: Node, p=None):
    import anytree
    if t is None:
        return None

    n = anytree.Node(f"{t.key} h={t.height}", parent=p)
    debug_tree(t.left, n)
    debug_tree(t.right, n)
    return n

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


    update_statistic(y)
    update_statistic(x)


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

    update_statistic(x)
    update_statistic(y)

def select(t: Node, nth):
    rank = t.left.size + 1 if t.left is not None else 1
    if nth == rank:
        return t.key
    elif nth < rank:
        return select(t.left, nth)
    else: # nth > rank
        return select(t.right, nth - rank)




def skew(t: Node) -> int:
    if t is None:
        return 0

    match t.left, t.right:
        case None, None: return 0
        case left, None: return -left.height
        case None, right: return right.height
        case left, right: return right.height - left.height

def check_and_fix_subtree(t: Node):
    x = t
    skew_metric = skew(x)
    assert skew_metric in [-2, -1, 0, 1, 2]
    if skew_metric not in [-2, 2]:
        return
    else:
        fixup_subtree(t)

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
def transplant(u: Node, v: Node | None):
    if u == u.parent.left:
        u.parent.left = v
    else: # u == u.parent.right:
        u.parent.right = v

    if v is not None:
        v.parent = u.parent


"""
Assuming all levels below tree t are height balanced, fix any invariants that t might have violated, and all of t's parent tree.
"""
def fixup_tree(t: Node | Root):
    if t.parent == t:
        return
    update_statistic(t)
    skew_metric = skew(t)

    if skew_metric not in [-1, 0, 1]:
        fixup_subtree(t)

    if t.parent != t: # stop at root node
        fixup_tree(t.parent)

def update_statistic(t: Node):
    update_height(t)
    update_size(t)

def update_height(t: Node | None):
    left = t.left.height if t.left else 0
    right = t.right.height if t.right else 0

    t.height = 1 + max(left, right)

def update_size(t: Node):
    left = t.left.size if t.left else 0
    right = t.right.size if t.right else 0

    t.size = left + right + 1

#################### TESTS  #########################
def test_single_node():
    t = Root()
    t.insert(5)
    assert t.left.key == 5

def test_insert_sorted():
    t = Root()
    t.insert(1)
    assert t.left.key == 1

    t.insert(2)
    assert t.left.key == 1

    t.insert(3)

    t = t.left
    assert t.key == 2
    assert t.left.key == 1
    assert t.right.key == 3


def test_insert_reversed():
    t = Root()
    t.insert(3)
    t.insert(2)
    t.insert(1)

    t.traverse()
    t.debug_tree()

def test_delete_stuff():
    t = Root()
    t.insert(3)
    t.insert(2)
    t.insert(1)

    t.delete(2)
    t.debug_tree("debug/WRONG!.png")
    t.traverse()

def test_delete_stuffv2():
    t = Root()
    for i in range(30):
        t.insert(i)
    t.debug_tree()

    to_delete = [5, 1, 26, 9, 28, 19, 27, 3, 18, 24, 15, 10, 23, 16, 13, 11, 12, 2, 14, 8, 29, 6, 25, 0, 4, 17, 22, 21, 20, 7]

    for i, e in enumerate(to_delete):
        try:
            t.delete(e)
            t.debug_tree(f"debug/tree-{i}-after-{e}.png")
        except AssertionError:
            print(f"failed on ={e} in {to_delete}")
            print(t.left)
            raise


    t.traverse()

def test_delete_stuff_extreme():
    n = 1000
    t = Root()
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
def test_delete_root():
    t = Root()
    for i in range(100):
        t.insert(i)

    for i in range(100):
        t.delete(t.left.key)
    t.traverse()

def test_insert_many():
    t = Root()
    l = list(range(100))
    random.shuffle(l)

    for i in l:
        t.insert(i)
    t.debug_tree()


def test_find_median():
    t = Root()
    t.insert(-1)
    t.insert(-2)
    t.insert(-3)
    t.insert(-4)
    n = t.left.size
    print(t.left.size)
    upper_median = ceil((n + 1) / 2)
    lower_median = floor((n + 1) / 2)
    print(f"{upper_median=}, {lower_median=}")


if __name__ == "__main__":
    pass




