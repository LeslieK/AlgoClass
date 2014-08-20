class WeightedQuickUnionUF(object):
    """
    connects tree with smaller size to root of tree with larger size
    """
    def __init__(self, N):
        self._id = [i for i in range(N)]
        self._size = [1 for i in range(N)]
        self._count = N

    def newSite(self):
        """
        create a new set of 1 element
        """
        new_site = sum(self._size)
        self._id.append(new_site)
        self._size.append(1)
        self._count += 1
        return new_site

    def size(self, c):
        """
        return the size of a component
        """
        return self._size[c]

    def count(self):
        """
        return the total number of elements
        """
        return self._count

    def connected(self, p, q):
        """
        return true if in the same set
        """
        return self.find(p) == self.find(q)

    def find(self, p):
        """
        returns component id (root)
        """
        while p != self._id[p]:
            p = self._id[p]
        return p

    def union(self, p, q):
        """
        connect 2 disjoint sets
        """
        i = self.find(p)
        j = self.find(q)
        if i == j:
            # already connected
            return
        if self._size[i] < self._size[j]:
            self._id[i] = j
            self._size[j] += self._size[i]
            self._size[i] = 0
        else:
            self._id[j] = i
            self._size[i] += self._size[j]
            self._size[j] = 0
        self._count -= 1

class RankQuickUnionUF(object):
    """
    connects tree with lower rank to root of tree with greater rank
    """
    def __init__(self, N):
        self._id = [i for i in range(N)]
        self._rank = [0 for i in range(N)]
        self._count = N

    def newSite(self):
        """
        create a new set of 1 element
        """
        new_site = sum(self._size)
        self._id.append(new_site)
        self._rank.append(0)
        self._count += 1
        return new_site

    def rank(self, i):
        """
        return the rank of a node
        """
        return self._rank[i]

    def count(self):
        """
        return the total number of components
        """
        return self._count

    def connected(self, p, q):
        """
        return true if in the same set
        """
        return self.find(p) == self.find(q)

    #def find(self, p):
    #    """
    #    returns component id (root)
    #    """
    #    while p != self._id[p]:
    #        p = self._id[p]
    #    return p

    def find(self, p):
        """
        returns component id (root)
        """
        while p != self._id[p]:
            # path compression by half
            self._id[p] = self._id[self._id[p]]
            p = self._id[p]
        return p

    #def find(self, p):
    #    """
    #    returns component id (root)
    #    """
    #    x = p
    #    while p != self._id[p]:
    #        p = self._id[p]
    #    # p is root
    #    # 2nd pass for path compression
    #    while x != p:
    #        self._id[x] = p
    #        x = self._id[x]
    #    return p

    def union(self, p, q):
        """
        connect 2 disjoint sets
        """
        i = self.find(p)
        j = self.find(q)
        if i == j:
            # already connected
            return
        if self._rank[i] < self._rank[j]:
            self._id[i] = j
            self._rank[j] += 1
        else:
            self._id[j] = i
            self._rank[i] += 1
        self._count -= 1