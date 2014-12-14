from collections import deque
from register import register
class freeList:
    def __init__(self):
        self.queue = deque()
        self.maxSize = 64
        self.busyTable = [0]*self.maxSize
        for i in range(self.maxSize):
            new_reg = register('P', i)
            self.queue.append(new_reg)
    
    def setBusyBit(self, index, value):
        self.busyTable[index] = value
        
    def getBusyBit(self, index):
        return self.busyTable[index]
        
    def popReg(self):
        # may cause exception if no more element in the queue.
        toPop = self.queue[0]
        toPop.setBusyBit(1)
        tag = toPop.getTag()
        self.setBusyBit(tag, 1)
        self.queue.popleft()
        return toPop
        
    def addReg(self, reg):
        self.queue.append(reg)
        reg.setBusyBit(0)
        tag = reg.getTag()
        self.setBusyBit(tag, 0)
        # WATCH OUT: the busy bit is not set to 0 upon its return to the freeList
        # but upon its value is written. (so that we can broadcast the value)
        
    def getNumFree(self):
        return len(self.queue)