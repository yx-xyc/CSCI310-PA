class Node(object):
    def __init__(self):
        self.guide = None
        # guide points to max key in subtree rooted at node


class InternalNode(Node):
    def __init__(self):
        Node.__init__(self)
        self.child0 = None
        self.child1 = None
        self.child2 = None
        # child0 and child1 are always non-none
        # child2 is none iff node has only 2 children


class LeafNode(Node):
    def __init__(self):
        Node.__init__(self)
        self.value = None
        # guide points to the key


class TwoThreeTree:
    def __init__(self):
        self.root = None
        self.height = -1


class WorkSpace:
    def __init__(self):
        self.newNode = None
        self.offset = None
        self.guideChanged = None
        self.scratch = [None] * 4


def insert(key, value, tree):
    # insert a key value pair into tree (overwrite existsing value
    # if key is already present)

    h = tree.height

    if h == -1:
        newLeaf = LeafNode()
        newLeaf.guide = key
        newLeaf.value = value
        tree.root = newLeaf
        tree.height = 0

    else:
        ws = doInsert(key, value, tree.root, h)

        if ws != None and ws.newNode != None:
            # create a new root

            newRoot = InternalNode()
            if ws.offset == 0:
                newRoot.child0 = ws.newNode
                newRoot.child1 = tree.root

            else:
                newRoot.child0 = tree.root
                newRoot.child1 = ws.newNode

            resetGuide(newRoot)
            tree.root = newRoot
            tree.height = h + 1


def doInsert(key, value, p, h):
    # auxiliary recursive routine for insert

    if h == 0:
        # we're at the leaf level, so compare and
        # either update value or insert new leaf

        leaf = p  #downcast (unnecessary in python)
        cmp = 0
        if key < leaf.guide:
            cmp = -1
        elif key > leaf.guide:
            cmp = 1

        if cmp == 0:
            leaf.value = value
            return None

        # create new leaf node and insert into tree
        newLeaf = LeafNode()
        newLeaf.guide = key
        newLeaf.value = value

        offset = 1
        if cmp < 0:
            offset = 0
        # offset == 0 => newLeaf inserted as left sibling
        # offset == 1 => newLeaf inserted as right sibling

        ws = WorkSpace()
        ws.newNode = newLeaf
        ws.offset = offset
        ws.scratch = [None] * 4

        return ws

    else:
        q = p  # downcast (unnecessary in python)
        pos = 2
        ws = None

        if key <= q.child0.guide:
            pos = 0
            ws = doInsert(key, value, q.child0, h - 1)

        elif key <= q.child1.guide or q.child2 is None:
            pos = 1
            ws = doInsert(key, value, q.child1, h - 1)

        else:
            pos = 2
            ws = doInsert(key, value, q.child2, h - 1)
        if ws != None:
            if ws.newNode != None:
                # make ws.newNode child # pos + ws.offset of q
                sz = copyOutChildren(q, ws.scratch)

                ws.scratch.insert(pos + ws.offset, ws.newNode)

                if sz == 2:
                    ws.newNode = None
                    ws.guideChanged = resetChildren(q, ws.scratch, 0, 3)
                else:
                    ws.newNode = InternalNode()
                    ws.offset = 1
                    resetChildren(q, ws.scratch, 0, 2)
                    resetChildren(ws.newNode, ws.scratch, 2, 2)

            elif ws.guideChanged:
                ws.guideChanged = resetGuide(q)

        return ws


def copyOutChildren(q, x):
    # copy children of q into x, and return # of children

    sz = 2
    x[0] = q.child0
    x[1] = q.child1
    if q.child2 != None:
        x[2] = q.child2
        sz = 3

    return sz


def resetGuide(q):
    # reset q.guide, and return true if it changes.

    oldGuide = q.guide
    if q.child2 != None:
        q.guide = q.child2.guide
    else:
        q.guide = q.child1.guide

    return q.guide != oldGuide


def resetChildren(q, x, pos, sz):
    # reset q's children to x[pos..pos+sz), where sz is 2 or 3.
    # also resets guide, and returns the result of that

    q.child0 = x[pos]
    q.child1 = x[pos + 1]

    if sz == 3:
        q.child2 = x[pos + 2]
    else:
        q.child2 = None

    return resetGuide(q)


def driverProgram():
    database_size = int(input())
    keys = []
    values = []
    for i in range(database_size):
        aline = input()
        seperated = aline.split(" ")
        keys.append(seperated[0])
        values.append(seperated[1])
    
    command_size = int(input())
    command1 = []
    command2 = []
    for j in range(command_size):
        aline = input()
        seperated = aline.split(" ")
        command1.append(seperated[0])
        command2.append(seperated[1])

    print(keys,"\n",values,"\n",command1,"\n",command2)

def printRange1(p,x,y,h,lo):
    if x > y:
        x,y = y,x
    if h == 0:
        if x <= p.guide <= y:
            print(p.guide,p.value)
            return
        else:
            return
    hi = p.guide
    if y <= lo:
        return
    if hi < x:
        return 
    
    printRange1(p.child0,x,y,h-1,lo)
    printRange1(p.child1,x,y,h-1,p.child0.guide)
    if p.child2 != None:
        printRange1(p.child2,x,y,h-1,p.child1.guide)

def main():
    #negative_infinity = float('-inf')
    #driver_program()
    twoThreeTree = TwoThreeTree()
    database_size = int(input())
    for i in range(database_size):
        aline = input()
        seperated = aline.split(" ")
        insert(seperated[0],seperated[1],twoThreeTree)

    command_size = int(input())
    for j in range(command_size):
        aline = input()
        seperated = aline.split(" ")
        printRange1(twoThreeTree.root,seperated[0],seperated[1],twoThreeTree.height,'a')

    
if __name__ == "__main__":
    main()
