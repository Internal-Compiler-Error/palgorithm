from math import ceil, floor

# float rather than int so median() can average two keys; ints are accepted too.
type Key = float


class Root:
    def __init__(self) -> None:
        self.child: Node | None = None
        self.parent: Root = self

    def traverse(self) -> None:
        l: list[Key] = []
        traverse(self.left, l)
        assert l == sorted(l)

    @property
    def left(self) -> Node | None:
        return self.child

    @left.setter
    def left(self, value: Node | None) -> None:
        self.child = value

    @property
    def right(self) -> Node | None:
        return self.child

    @right.setter
    def right(self, value: Node | None) -> None:
        self.child = value

    def select(self, nth: int) -> Key:
        t = self.child
        return select(t, nth)

    def insert(self, key: Key) -> None:
        """
        Insert a new node at the tree rooted at t
        """
        if self.child is None:
            self.child = Node(self, key)
            return

        parent = self.child
        t: Node | None = self.child
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

    def delete(self, key: Key) -> None:
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

        if z is None: return # key doesn't exist
        if parent is None: return # deleting the root node

        if z.left is None:
            transplant(z, z.right)
            fixup_tree(parent)
            return
        elif z.right is None:
            transplant(z, z.left)
            fixup_tree(parent)
            return
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
                fixup_tree(old_parent)
            return

    def median(self) -> float:
        if self.child is None:
            raise ValueError("median of an empty tree")
        n = self.child.size

        upper = ceil((n + 1) / 2)
        lower = floor((n + 1) / 2)

        return (self.select(upper) + self.select(lower)) / 2

    def debug_tree(self, name: str = "debug/tree.png") -> None:
        t = debug_tree(self.left)

        if t is None:
            return
        import anytree.exporter  # pyright: ignore[reportMissingTypeStubs]
        anytree.exporter.UniqueDotExporter(t).to_picture(name)  # pyright: ignore[reportUnknownMemberType]

class Node:
    def __init__(self, parent: Node | Root, key: Key) -> None:
        self.left: Node | None = None
        self.right: Node | None = None
        self.parent: Node | Root = parent

        self.key: Key = key
        self.height: int = 1

        # augmented zone
        self.size: int = 1

    def rank(self) -> int:
        r = 1 + self.left.size if self.left else 1
        y: Node | Root = self

        # loop until we reach root
        while y.parent != y:
            if y.parent.right == y:
                r += y.parent.left.size if y.parent.left else 0
            y = y.parent

        return r


def traverse(t: Node | None, sink: list[Key]) -> None:
    if t is None:
        return

    traverse(t.left, sink)
    sink.append(t.key)
    traverse(t.right, sink)

def debug_tree(t: Node | None, p=None):
    import anytree
    if t is None:
        return None

    n = anytree.Node(f"{t.key} h={t.height}", parent=p)
    debug_tree(t.left, n)
    debug_tree(t.right, n)
    return n

def rot_right(tree: Node) -> None:
    """
                       y
                  x       C
               A     B
    into:
                       x
                    A       y
                         B     C
    """
    y = tree
    tree_parent = y.parent
    x = y.left
    assert x is not None, "rot_right needs a left child"
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


def rot_left(tree: Node) -> None:
    """
                       x
                    A       y
                         B     C
    into:
                       y
                  x       C
               A     B
    """
    x = tree
    y = x.right
    assert y is not None, "rot_left needs a right child"
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

def select(t: Node | None, nth: int) -> Key:
    if t is None:
        raise IndexError(f"no element of rank {nth}")
    rank = t.left.size + 1 if t.left is not None else 1
    if nth == rank:
        return t.key
    elif nth < rank:
        return select(t.left, nth)
    else: # nth > rank
        return select(t.right, nth - rank)

def skew(t: Node | None) -> int:
    if t is None:
        return 0

    match t.left, t.right:
        case None, None: return 0
        case left, None: return -left.height
        case None, right: return right.height
        case left, right: return right.height - left.height

def check_and_fix_subtree(t: Node) -> None:
    x = t
    skew_metric = skew(x)
    assert skew_metric in [-2, -1, 0, 1, 2]
    if skew_metric not in [-2, 2]:
        return
    else:
        fixup_subtree(t)

def fixup_subtree(t: Node) -> None:
    """
    Assuming subtree t violates the height balance property, fixup the invariants using rotates
    """
    x = t
    skew_metric = skew(x)
    assert skew_metric in [-2, 2]
    if skew_metric == 2:
        z = x.right
        assert z is not None
        z_skew = skew(z)
        assert z_skew in [-1, 0, 1]

        match z_skew:
            case -1: rot_right(z); rot_left(x)
            case  0: rot_left(x)
            case  1: rot_left(x)
    else: # skew_metric == -2
        z = x.left
        assert z is not None
        z_skew = skew(z)
        assert z_skew in [-1, 0, 1]
        match z_skew:
            case -1: rot_right(x)
            case  0: rot_right(x)
            case  1: rot_left(z); rot_right(x)

def transplant(u: Node, v: Node | None) -> None:
    """
    Replaces the subtree rooted at u with the one rooted at v
    """
    if u == u.parent.left:
        u.parent.left = v
    else: # u == u.parent.right:
        u.parent.right = v

    if v is not None:
        v.parent = u.parent


def fixup_tree(t: Node | Root) -> None:
    """
    Assuming all levels below tree t are height balanced, fix any invariants that t might have violated, and all of t's parent tree.
    """
    if isinstance(t, Root):
        return
    update_statistic(t)
    skew_metric = skew(t)

    if skew_metric not in [-1, 0, 1]:
        fixup_subtree(t)

    if t.parent != t: # stop at root node
        fixup_tree(t.parent)

def update_statistic(t: Node) -> None:
    update_height(t)
    update_size(t)

def update_height(t: Node) -> None:
    left = t.left.height if t.left else 0
    right = t.right.height if t.right else 0

    t.height = 1 + max(left, right)

def update_size(t: Node) -> None:
    left = t.left.size if t.left else 0
    right = t.right.size if t.right else 0

    t.size = left + right + 1
