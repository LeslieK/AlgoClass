"""
Huffman Encoding (another greedy algorithm)
"""
from indexMinPQ import MinPQ
R = 128  # size of alphabet

class NodeT(object):
    """
    a node in a trie
    """
    def __init__(self, ch, freq, left, right):
        self.freq = freq
        self.ch = ch
        self.left = left
        self.right = right

    def isLeaf(self):
        if self.left is None and self.right is None:
            return True
        else:
            return False

    def __lt__(self, that):
        if that is None:
            raise TypeError
        return self.freq < that.freq

    def __le__(self, that):
        if that is None:
            raise TypeError

class Trie(object):
    """
    a binary trie data structure
    huffman encodes ascii-encoded strings
    uses a priority queue (heap)
    """
    def __init__(self, freq):
        pq = MinPQ()
        for c in range(R):
            if freq[c] > 0:
                pq.insert(NodeT(c, freq[c], None, None))

        while pq.size() > 1:
            x = pq.delMin()
            y = pq.delMin()
            parent = NodeT("\0", x.freq + y.freq, x, y)
            pq.insert(parent)
        self.rootNode = pq.delMin()  # returns the root node of the trie

    def root(self):
        return self.rootNode

class Trie2(object):
    """
    a binary trie data structure
    huffman encodes ascii-encoded strings
    uses 2 queues (lists)
    """
    def __init__(self, freq):
        d1 = []
        for i, f in enumerate(freq):
            if f > 0:
                d1.append(NodeT(i, f, None, None))
        
        d1.sort() # top of queue is at front of list
        d2 = []  

        # set queue ptrs to front of lists
        self.i1 = 0
        self.i2 = 0

        # set sizes of queues
        self.lenq1 = len(d1)
        self.lenq2 = 0

        while self.lenq1 - self.i1 + self.lenq2 - self.i2 > 1:
            parent = self.merge(d1, d2)
            d2.append(parent)
            self.lenq2 += 1
        self.rootNode = d2[self.i2]

    def root(self):
        return self.rootNode

    def merge(self, q1, q2):
        """
        merge 2 symbols and return parent symbol
        q1: queue of sorted frequencies
        q2: queue of sorted merged nodes
        """
        res = []
        count = 2
        while count > 0:
            if self.i1 < self.lenq1 and self.i2 < self.lenq2:
                x, i = min((q1[self.i1], 1), (q2[self.i2], 2))
                if i == 1:
                    self.i1 += 1
                else:
                    self.i2 += 1
            elif self.i1 < self.lenq1:
                x = q1[self.i1]
                self.i1 += 1
            elif self.i2 < self.lenq2:
                x = q2[self.i2]
                self.i2 += 1
            elif count == 2:
                # q1 and q2 are empty
                return None
            res.append(x)
            count -= 1
        parent = NodeT("\0", res[0].freq + res[1].freq, res[0], res[1])
        return parent

def frequency(document):
    """
    returns a character-indexed array of frequencies in input document
    """
    freq = [0] * R
    with open(document, 'r', encoding='ascii') as f:
        words = (line.strip() for line in f)
        for word in words:
            for c in word:
                freq[ord(c)] += 1
    return freq

def frequencyST(astring):
    freq = [0] * R
    words = astring.strip().split()
    for word in words:
        for c in word:
            freq[ord(c)] += 1
    return freq

def buildCode(root):
    """
    build a code lookup table from a trie
    """
    code = [None] * R
    def helper(code, x, acc):
        if x is None: return
        if x.isLeaf():
            code[x.ch] = acc
            return
        helper(code, x.left, acc + '0')
        helper(code, x.right, acc + '1')

    helper(code, root, "")
    return code
        
########################################### 
if __name__ == "__main__":
    filename = "sowpods.txt"
    freq = frequency(filename)
    #freq = frequencyST("a" * 32 + "b" * 32 + "c" * 18 + "d" * 8 + "e" * 10)
    trie = Trie2(freq)
    code = buildCode(trie.root())
    code

