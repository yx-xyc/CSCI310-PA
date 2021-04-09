import fileinput
class Soldier:
    def __init__(self,name,score,pos):
        self.name=name
        self.score=score
        self.pos=pos

class MinHeap(object):

    def __init__(self,maxsize=100):
        self.size = 0
        self.heap = ['']*maxsize
        self.army={}

    def size(self):
        return self.size

    def insert(self, name,score):
        s=Soldier(name,score,self.size)
        self.army[name]=s
        self.heap[self.size] = name
        if self.size > 0:
            self.siftup(self.size)
        self.size += 1

    def siftup(self, index):
        parent_index = int((index - 1) / 2)
        if parent_index >= 0:
            if self.score(index) < self.score(parent_index):
                self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                self.army[self.heap[index]].pos,self.army[self.heap[parent_index]].pos=self.army[self.heap[parent_index]].pos,self.army[self.heap[index]].pos
                self.siftup(parent_index)

    def score(self,index):
        return self.army[self.heap[index]].score

    def extrace(self):
        if self.size < 0:
            raise Exception("Empty Heap")
        self.size -= 1
        value = self.heap[0]
        self.army[self.heap[0]].pos = -1
        self.heap[0] = self.heap[self.size]
        self.army[self.heap[self.size]].pos=0
        self.siftdown(0)
        return value

    def siftdown(self, root_index):
        min_index = root_index
        left = int(root_index * 2 + 1)
        right = int(root_index * 2 + 2)
        if left < self.size and  self.score(left)<self.score(min_index):
            min_index = left
        if right < self.size  and self.score(right) <self.score(min_index):
            min_index = right
        if root_index != min_index:
            self.heap[root_index], self.heap[min_index] = self.heap[min_index], self.heap[root_index]
            self.army[self.heap[root_index]].pos, self.army[self.heap[min_index]].pos = self.army[self.heap[
                min_index]].pos, self.army[self.heap[root_index]].pos
            self.siftdown(min_index)

    def select(self, standard):
        while True:
            s=self.score(0)
            if s<standard:
                self.extrace()
            else:
                break
        print(self.size)

    def improve(self,name,s):
        self.army[name].score+=s
        p=self.army[name].pos
        self.siftdown(p)

    def show(self):
        #for key,value in self.army.items():
            #print("key: ",key, "value",self.army[key].score,"pos", self.army[key].pos)
        #print(self.Heap)
        for each in self.heap:
            if each == "removed":
                continue
            else:
                print("key: ",self.army[each].name, "value:",self.army[each].score,"posS", self.army[each].pos)
def main():
    with fileinput.FileInput("input03.txt") as input:
        cmdNumber = int(input.readline())
        heap=MinHeap(cmdNumber)
        for i in range(cmdNumber):
            #print("########")
            s = input.readline().split(' ')
            heap.insert(s[0],int(s[1]))
        heap.show()
        m = int(input.readline())
        for j in range(m):
            #print("########")
            s = input.readline().split(' ')
            if len(s) == 3:
                heap.improve(s[1],int(s[2]))
            else:
                standard = int(s[1])
                heap.select(standard)
            heap.show()
            print("+++++++++++++++++++++++")

if __name__ == "__main__":
    main()