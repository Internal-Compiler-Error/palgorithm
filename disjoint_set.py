class DisjointSet:
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        self.rank = [0] * n
        self.n = n

    def merge(self, a, b):
        assert a < self.n
        assert b < self.n

        a = self.find(a)
        b = self.find(b)

        if a == b:
            return

        # ensure tree 'a' is at least as high or higher than tree 'b'
        if self.rank[a] < self.rank[b]:
            a, b = b, a

        # always attach the tree with the lesser height to the one with greater height, because we link it directly to
        # the root instead of some leaf, the height is at most worsened by one
        self.parent[b] = a
        if self.rank[a] == self.rank[b]:
            self.rank[a] += 1 # it now takes one more vertex, the root of a, to traverse down to leaves of b

    def find(self, a):
        assert a < self.n

        # a -> b -> c -> ... -> root
        while self.parent[a] != a:
            b = self.parent[a]
            c = self.parent[b]

            self.parent[a] = c # link 'a' to its grandparent
            a = b

        return a

    def same_set(self, a, b):
        assert a < self.n
        assert b < self.n
        return self.find(a) == self.find(b)
