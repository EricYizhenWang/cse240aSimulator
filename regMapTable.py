from freeList import freeList
class regMapTable:
    def __init__(self):
        self.maxSize = 32
        self.table = [0] * self.maxSize
        self.f = freeList()
        
    def getFreeList(self):
        return self.f
    
    def getNumFreeReg(self):
        return self.f.getNumFree()
    
    def getMapping(self, regLogicalIndex):
        return self.table[regLogicalIndex]
    
    def setMapping(self, regLogicalIndex, physicalReg):
        self.table[regLogicalIndex] = physicalReg
        
    def assignNewMapping(self, regLogicalIndex):
        # This function maps a logical register to a physical register 
        # It returns the old physical register associated with that logical 
        # register and update the mapping.
        old_value = self.table[regLogicalIndex]
        new_value = self.f.popReg()
        #self.table[regLogicalIndex] = new_value
        self.setMapping(regLogicalIndex, new_value)
        return [regLogicalIndex, old_value, new_value]
    
    
        