from freeList import freeList
class regMapTable:
    def __init__(self):
        self.maxSize = 32
        self.table = [0] * self.maxSize
    
    def getMapping(self, regLogicalIndex):
        return self.table[regLogicalIndex]
    
    def setMapping(self, regLogicalIndex, physicalReg):
        self.table[regLogicalIndex] = physicalReg
        

    
        