class Node(object):
    def __init__(self):
        self.guide = None
        self.value = 0

class InternalNode(Node):
    def __init__(self):
        Node.__init__(self)
        self.child0 = None
        self.child1 = None
        self.child2 = None

class LeafNode(Node):
    def __init__(self):
        Node.__init__(self)
