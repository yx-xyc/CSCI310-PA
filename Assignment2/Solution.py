import fileinput
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

        if q.value != 0:
            q.child0.value += q.value
            q.child1.value += q.value
            if q.child2 != None:
                q.child2.value += q.value
            q.value = 0

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

def addRange(p, x, y, h, lo, value):
    if x >= y:
        x,y = y,x
    if h == 0:
        if x <= p.guide <= y:
            p.value += value
            return
        else:
            return
    hi = p.guide
    if y <= lo:
        return
    if hi < x :
        return
    if x<= lo and hi < y:
        p.value += value
        return
    
    addRange(p.child0,x,y,h-1,lo,value)
    addRange(p.child1,x,y,h-1,p.child0.guide,value)
    if p.child2 != None:
        addRange(p.child2,x,y,h-1,p.child1.guide,value)

def lookup(p, h, key):
    value = 0
    for i in range(h):
        value += p.value
        if key <= p.child0.guide:
            p = p.child0
        elif p.child2 == None or key <= p.child1.guide:
            p = p.child1
        else:
            p = p.child2
    if key == p.guide:
        return value+p.value
    else:
        return -1
            
    
    if h == 0:
        if key == p.guide:
            return p.value
        else:
            return -1
    if key <= p.child0.guide and (lookup(p.child0, h-1, key)) != -1:
            return p.value+lookup(p.child0, h-1, key)
    elif key <= p.child1.guide and (lookup(p.child1, h-1, key)) != -1:
            return p.value+lookup(p.child1, h-1, key)
    elif p.child2 != None and key <= p.child2.guide and (lookup(p.child2, h-1, key)) != -1:
            return p.value+lookup(p.child2, h-1, key)
    else:
        return -1


def main():
    twoThreeTree = TwoThreeTree()
    with fileinput.FileInput("test2.in") as input:
        cmdNumber = input.readline()
        for i in range(int(cmdNumber)):
            line = input.readline()
            cmdList = line.split()
            if cmdList[0] == "1":
                insert(cmdList[1],int(cmdList[2]),twoThreeTree)
            elif cmdList[0] == "2":
                addRange(twoThreeTree.root,cmdList[1],cmdList[2],twoThreeTree.height,"0",int(cmdList[3]))
            elif cmdList[0] == "3":
                fee = lookup(twoThreeTree.root,twoThreeTree.height,cmdList[1])
                print(fee)


if __name__ == "__main__":
    main()
