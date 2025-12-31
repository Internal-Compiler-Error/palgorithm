from typing import Tuple


class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.parent = None

        self.key = None
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
def rot_right(tree: Node) -> Node:
    y = tree
    y_parent = y.parent
    x = y.left
    a = x.left
    b = x.right
    c = y.right

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

    y.parent = x
    x.parent = y_parent

    update_height(y)
    update_height(x)

    return x


"""
                   x 
                A       y          
                     B     C
into:
                   y
              x       C
           A     B

"""
def rot_left(tree: Node) -> Node:
    x = tree
    y = x.right
    a = x.left
    b = y.left
    c = y.right

    tree_parent = x.parent

    y.left = x
    x.parent = y

    y.right = c
    if c:
        c.parent = y

    x.left = a
    if a:
        a.parent = x

    x.right = b
    if b:
        b.parent = x

    y.parent = tree_parent
    update_height(x)
    update_height(y)

    return y


"""
Insert a new node at the tree rooted at t, returning the new root node
"""
def insert(t: Node | None, key) -> Node:
    parent = None
    while t:
        if t.key <= key:
            parent = t
            t = t.right
        else:  # t.key > key:
            parent = t
            t = t.left

    x = Node()
    x.key = key
    
    if parent is None:
        # empty tree, this is the first node
        x.height = 1
    else:
        if parent.key <= key:
            parent.right = x
            x.parent = parent
        else: # t.key > key:
            parent.left = x
            x.parent = parent

        x.height = 1
        

    return fixup_tree(x.parent, x)

def delete(t: Node, key) -> Node | None:
    root = t

    parent = None
    while t:
        if t.key < key:
            parent = t
            t = t.right
        elif t.key > key:
            parent = t
            t = t.left
        else: # t.key == key
            break
    
    if t is None: print("trying to delete a node that doesn't exist, not allowed for this implementation")
    if parent is None: return None # deleting the root node

    if t.left is None:
        t_parent = t.parent
        t_child = t.right
        transplant(root, t, t.right)
        return fixup_tree(t_parent,  t_child)
    elif t.right is None:
        t_parent = t.parent
        t_child = t.left
        transplant(root, t, t.left)
        return fixup_tree(t_parent, t_child)
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

        return fixup_tree(y.right, y.right.right)



def skew(t: Node) -> int:
    if t is None:
        return 0

    match t.left, t.right:
        case None, None: return 0
        case left, None: return -left.height
        case None, right: return right.height
        case left, right: return right.height - left.height

"""
Assuming subtree t violates the height balance property, fixup the invariants using rotates, returning the new node 
that previously occupied at t
"""
def fixup_subtree(t: Node) -> Node:
    x = t
    skew_metric = skew(x)
    assert skew_metric in [-2, 2]
    if skew_metric == 2:
        z = x.right
        z_skew = skew(z)
        assert z_skew in [-1, 0, 1]

        match z_skew:
            case -1:
                rot_right(z)
                return rot_left(x)
            case 0: return rot_left(x)
            case 1: return rot_left(x)
    else: # skew_metric == -2
        z = x.left
        z_skew = skew(z)
        assert z_skew in [-1, 0, 1]
        match z_skew:
            case -1: return rot_right(x)
            case 0: return rot_right(x)
            case 1:
                rot_left(z)
                return rot_right(x)

def transplant(t: Node, u: Node, v: Node | None):
    if u.parent is None:
        pass
    elif u == u.parent.left:
        u.parent.left = v
    else: # u == u.parent.right:
        u.parent.right = v

    if v is not None:
        v.parent = u.parent


"""
Assuming all levels below tree t are height balanced, fix any invariants that t might have, and all of t's parent tree,
returning the overall root tree node 
"""
def fixup_tree(t: Node | None, t_child: Node) -> Node:
    if t is None:
        return t_child

    update_height(t)
    skew_metric = skew(t)

    if skew_metric not in [-1, 0, 1]:
        t = fixup_subtree(t)
        return fixup_tree(t.parent, t)
    else:
        return fixup_tree(t.parent, t)


def update_height(t: Node | None):
    left = t.left.height if t.left else 0
    right = t.right.height if t.right else 0

    t.height = 1 + max(left, right)

def single_node():
    t = None
    t = insert(t, 5)
    assert t.key == 5

def insert_sorted():
    t = None
    t = insert(t, 1)
    assert t.key == 1

    t = insert(t, 2)
    assert t.key == 1

    t = insert(t,  3)

    assert t.key == 2
    assert t.left.key == 1
    assert t.right.key == 3

def traverse(t: Node):
    if t is None:
        return

    traverse(t.left)
    print(t.key)
    traverse(t.right)

def insert_reversed():
    t = None
    t = insert(t, 3)
    t = insert(t, 2)
    t = insert(t, 1)

    traverse(t)

def delete_stuff():
    t = None
    t = insert(t, 3)
    t = insert(t, 2)
    t = insert(t, 1)

    t = delete(t, 3)
    traverse(t)



if __name__ == "__main__":
    #single_node()
    #insert_sorted()
    #insert_reversed()




