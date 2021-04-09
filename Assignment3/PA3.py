class Soldier:
    def __init__(self,name,score,pos):
        self.name=name
        self.score=score
        self.pos=pos

class MinHeap(object):

    def __init__(self,maxsize=100):
        self.length = 0
        self.array = ['']*maxsize
        self.soldier={}

    def _length__(self):
        return self.length

    def add(self, name,score):
        s=Soldier(name,score,self.length)
        self.soldier[name]=s
        self.array[self.length] = name
        if self.length > 0:
            self._siftup(self.length)
        self.length += 1

    def getScore(self,index):
        return self.soldier[self.array[index]].score

    def _siftup(self, index):
        parent_index = int((index - 1) / 2)
        if parent_index >= 0:
            if self.getScore(index) < self.getScore(parent_index):
                self.array[index], self.array[parent_index] = self.array[parent_index], self.array[index]
                self.soldier[self.array[index]].pos,self.soldier[self.array[parent_index]].pos=self.soldier[self.array[parent_index]].pos,self.soldier[self.array[index]].pos
                self._siftup(parent_index)

    def _siftdown(self, root_index):
        min_index = root_index
        left = int(root_index * 2 + 1)
        right = int(root_index * 2 + 2)
        if left < self.length and  self.getScore(left)<self.getScore(min_index):
            min_index = left
        if right < self.length  and self.getScore(right) <self.getScore(min_index):
            min_index = right
        if root_index != min_index:
            self.array[root_index], self.array[min_index] = self.array[min_index], self.array[root_index]
            self.soldier[self.array[root_index]].pos, self.soldier[self.array[min_index]].pos = self.soldier[self.array[
                min_index]].pos, self.soldier[self.array[root_index]].pos
            self._siftdown(min_index)
    
    def extrace(self):
        if self.length < 0:
            raise Exception("Empty Heap")
        self.length -= 1
        value = self.array[0]
        self.soldier[self.array[0]].pos = -1
        self.array[0] = self.array[self.length]
        self.soldier[self.array[self.length]].pos=0
        self._siftdown(0)
        return value

    def select(self, standard):
        while True:
            s=self.getScore(0)
            if s<standard:
                self.extrace()
            else:
                break
        print(self.length)

    def impove(self,name,s):
        self.soldier[name].score+=s
        p=self.soldier[name].pos
        self._siftdown(p)

n = int(input())
heap=MinHeap(n)
for i in range(n):
    s = input().split(' ')
    heap.add(s[0],int(s[1]))
n = int(input())
for i in range(n):
    s = input().split(' ')
    if len(s) == 3:
        heap.impove(s[1],int(s[2]))
    else:
        standard = int(s[1])
        heap.select(standard)
