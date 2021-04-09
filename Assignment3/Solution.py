import fileinput
class Node(object):
    def __init__(self,name="null",score=0):
        self.name = name
        self.score = score

class MinHeap(object):
    def __init__(self):
        self.size = 0
        self.Heap = [Node("rooot",-999999)]
        self.FRONT = 1

    def parent(self,pos):
        return pos//2

    def leftChild(self, pos):
        return (2*pos)

    def rightChild(self,pos):
        return (2*pos)+1

    def isLeaf(self,pos):
        if pos >= (self.size//2) and pos <= self.size:
            return True
        return False

    def swap(self,fpos,spos):
        self.Heap[fpos],self.Heap[spos] = self.Heap[spos],self.Heap[fpos]

    def minHeapify(self, pos):
        if self.leftChild(pos) > self.size:
            return
        if self.rightChild(pos) > self.size:
            if self.Heap[pos].score > self.Heap[self.leftChild(pos)].score:
                self.swap(pos, self.leftChild(pos))
                self.minHeapify(self.leftChild(pos))
        else:
            if (self.Heap[pos].score > self.Heap[self.leftChild(pos)].score or \
                self.Heap[pos].score > self.Heap[self.rightChild(pos)].score):
                if self.Heap[self.rightChild(pos)].score > self.Heap[self.leftChild(pos)].score:
                    self.swap(pos, self.leftChild(pos))
                    self.minHeapify(self.leftChild(pos))
                else:
                    self.swap(pos, self.rightChild(pos))
                    self.minHeapify(self.rightChild(pos))
    
    def insert(self, element):
        if len(self.Heap) == self.size + 1: 
            self.size = self.size + 1
            self.Heap.append(element)
        else:
            self.size = self.size + 1
            self.Heap[self.size] = element

        newNode = self.size
        if self.size >1:
            #print(self.Heap[newNode].score,self.Heap[self.parent(newNode)].score)
            while self.Heap[newNode].score < self.Heap[self.parent(newNode)].score:
                self.swap(newNode, self.parent(newNode))
                newNode = self.parent(newNode)
                #print("*")
    def min(self):
        return self.Heap[self.FRONT].score

    def show(self):
        print("####################")
        for i in range(1,self.size+1):
            print(self.Heap[i].name,self.Heap[i].score)
    def delMin(self):
        popped = Node(self.Heap[self.FRONT].name,self.Heap[self.FRONT].score)
        self.Heap[self.FRONT].score = self.Heap[self.size].score
        self.Heap[self.FRONT].name = self.Heap[self.size].name
        #print("deleted number:",self.Heap[self.size].score)
        #self.Heap.remove(self.Heap[self.size])
        self.size -= 1
        #print("****")
        #self.show()
        #print("****")
    
        self.minHeapify(self.FRONT)
        #self.show()
        return popped
        #print("########################")
def main():
    dataBase = {}
    survivor = {}
    minheap = MinHeap()
    with fileinput.FileInput("input03.txt") as input:
        cmdNumber = input.readline()
        k = int(cmdNumber)
        for i in range(int(cmdNumber)):
            line = input.readline()
            data = line.split()
            dataBase[data[0]] = int(data[1])
            survivor[data[0]] = True
            node = Node(data[0],int(data[1]))
            minheap.insert(node)
        cmdNumber = input.readline()
        #minheap.show()
        for j in range(int(cmdNumber)):
            line = input.readline()
            operations = line.split()
            if operations[0] == "1":
                dataBase[operations[1]] += int(operations[2])
                anode = Node(operations[1],dataBase[operations[1]])
                minheap.insert(anode)
            elif operations[0] == "2":
                while minheap.min()<int(operations[1]):
                    #print("lower restriction:",operations[1])
                    #print("should be deleted number:",minheap.min())
                    deleted = minheap.delMin()                   
                    #print(deleted.score)
                    #print(deleted.name,deleted.score)
                    #print(dataBase[deleted.name])
                    if dataBase[deleted.name]==deleted.score:
                        if survivor[deleted.name] != False:
                            survivor[deleted.name] = False
                            k = k - 1
                            #print("*************************",deleted.name,deleted.score,dataBase[deleted.name])
                #for i in dataBase.keys():
                #    print(i,dataBase[i])
                #minheap.show()    

                #print("the requrement for this term",operations[1])        
                print(k)
                '''
                counter = 0
                for value in survivor.values():
                    if value == True:
                        counter += 1
                        '''
                #print(dataBase)
                #print(survivor)
                #print(minheap.size)
            #minheap.show()




if __name__ == "__main__":
    main()