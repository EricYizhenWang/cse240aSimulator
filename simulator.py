from activeList import activeList
from freeList import freeList
from integerQueue import integerQueue
from regMapTable import regMapTable
from register import register
from instruction import instruction
from ALU import ALU

class simulator:
    def __init__(self):
        self.activeList = activeList()
        self.freeList = freeList()
        self.integerQueue = integerQueue()
        self.regMapTable = regMapTable()
        self.ALU = ALU()
        self.initializeRegMap()
        
    def initializeRegMap(self):
        for i in range(32):
            self.regMapTable.setMapping(i, self.freeList.queue[0])
            self.freeList.popReg()
    
    def assignNewMapping(self, regLogicalIndex):
            # This function maps a logical register to a physical register 
            # It returns the old physical register associated with that logical 
            # register and update the mapping.
            old_value = self.regMapTable.table[regLogicalIndex]
            new_value = self.freeList.popReg()
            print new_value.getTag()
            self.regMapTable.setMapping(regLogicalIndex, new_value)
            self.freeList.setBusyBit(new_value.getTag(), 1)
            return [regLogicalIndex, old_value, new_value]
        
    def resolveOperand(self, insr):
        # This function resolves the insr's arguments into physical registers
        # 0 means the value is pre-loaded
        args = insr.getArgs()
        type_insr = insr.getType()
        if type_insr == 'I':
            #resolveTheOperand
            print 'This is executed', args
            for i in range(1,3):
                new_arg = self.regMapTable.getMapping(args[i])
                print i, new_arg.getTag()
                insr.setArgs_i(new_arg, i)
            #resolveTheDestination
            newMapInfo = self.assignNewMapping(args[0])
            insr.setRegMapInfo(newMapInfo[0:2])
            insr.setArgs_i(newMapInfo[2],0)
        
    def processInsr(self, insr):
        executedInsr = self.ALU.popInstruction()
        if executedInsr != 0:
            tag = executedInsr.getTag()
            self.activeList.setInsrDoneBit(executedInsr)
        if len(self.integerQueue.queue)>0:
            popedInsr = self.integerQueue.sendInsrForExecution()
        if len(self.activeList.queue) > 0:
            self.activeList.graduateInstruction()
        
        self.resolveOperand(insr)
        self.activeList.addInstruction(insr)
        self.integerQueue.addInstruction(insr)
        self.ALU.addInstruction(insr)
        
    
    
        
        
        
        
        
        