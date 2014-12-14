from collections import deque
from basicComponents import activeList, freeList, integerQueue, \
     regMapTable, register, instruction, ALU, insrBuffer, FPunit, FPqueue

class simulator:
    def __init__(self):
        self.activeList = activeList()
        self.freeList = freeList()
        self.integerQueue = integerQueue()
        self.FPqueue = FPqueue()
        self.regMapTable = regMapTable()
        self.ALU = ALU()
        self.FPA = FPunit('A')
        self.initializeRegMap()
        self.insrSet = deque()
        self.fetchedList = insrBuffer()
        self.decodedList = insrBuffer()
        
        self.fetch_r = deque()
        self.decode_r = deque()
        self.issue_r = []
        self.execution_r = []
     
    def setInsrSet(self, insrSet):
        self.insrSet = insrSet
    
    def getElemFromInsrSet(self):
        if len(self.insrSet)>0:
            print len(self.insrSet)
            return self.insrSet.popleft()
    
    def updateHistoryInInsrSet(self):
        for i in range(len(self.insrSet)):
            insr = self.insrSet[i]
            insr.addHistory(' ')
        
    def initializeRegMap(self):
        for i in range(32):
            self.regMapTable.setMapping(i, self.freeList.queue[0])
            reg = self.freeList.popReg()
            reg.setBusyBit(0)
    
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
        args = insr.getArgs()
        type_insr = insr.getType()
        if (type_insr == 'I') or (type_insr == 'A'):
            #resolveTheOperand
            #print 'This is executed', args
            for i in range(1,3):
                new_arg = self.regMapTable.getMapping(args[i])
                print i, new_arg.getTag()
                insr.setArgs_i(new_arg, i)
            #resolveTheDestination
            newMapInfo = self.assignNewMapping(args[0])
            insr.setRegMapInfo(newMapInfo[0:2])
            insr.setArgs_i(newMapInfo[2],0)
        
    def fetch_calc(self):
        insrSet = deque()
        #print 'min(4,len)', min(4, len(self.insrSet))
        for i in range(min(4, len(self.insrSet))):
            #get instructions from the insrSet
            new_elem = self.getElemFromInsrSet()
            new_elem.addHistory('F')
            insrSet.append(new_elem)
            
        self.fetch_r = insrSet
    
    def fetch_edge(self):
        insrSet = self.fetch_r
        self.fetchedList.addInsrSet(insrSet)
    
    def decode_calc(self):
        print 'decoding'
        decode_q = deque()
        l = min(4, self.fetchedList.getLength())
        for i in range(l):
            insr = self.fetchedList.popInstruction()
            #Assume Integer operation now
            self.resolveOperand(insr)
            insr.addHistory('D')
            decode_q.append(insr)
        
        self.decode_r = decode_q
    
    def decode_edge(self):
        decode_q = self.decode_r
        self.decodedList.addInsrSet(decode_q)

    def issue_calc(self):
        print 'issueing'
        l = min(4, self.decodedList.getLength())
        toActiveList = deque()
        toIntegerQueue = deque()
        toFPqueue = deque()
        for i in range(l):
            insr = self.decodedList.popInstruction()
            insr_type = insr.getType()
            toActiveList.append(insr)
            #TODO: add different type of insr here
            if insr_type == 'I':
                toIntegerQueue.append(insr)
            elif (insr_type == 'A') or (insr_type == 'M'):
                toFPqueue.append(insr)
            insr.addHistory('I')
        self.issue_r = [toActiveList, toIntegerQueue, toFPqueue]
    
    def issue_edge(self):
        toActiveList, toIntegerQueue, toFPqueue = self.issue_r
        self.activeList.addInsrSet(toActiveList)
        self.integerQueue.addInsrSet(toIntegerQueue)
        self.FPqueue.addInsrSet(toFPqueue)
        
    def execution_calc(self):
        print 'execution'
        print 'ALUqueue length', self.ALU.getLength()
        insr = self.ALU.popInstruction()
        print 'insr=', insr
        if insr != 0:
            tag = insr.getTag()
            self.activeList.setInsrDoneBit(insr)
            insr.addHistory('E')
            
        insr = self.FPA.popInstruction()
        print insr
        if insr == None:
            pass
        else: 
            tag = insr.getTag()
            self.activeList.setInsrDoneBit(insr)
            #insr.addHistory('A')
            
        # get the refill units to ALU ready
        popedInsr = self.integerQueue.sendInsrForExecution()
        popedFPInsr = self.FPqueue.sendInsrForExecution()
        self.execution_r = [popedInsr, popedFPInsr]
        
    def execution_edge(self):
        # Then fill the pipeline with the next instruction
        #if (len(self.integerQueue.queue)>0) and (self.ALU.getLength() == 0):
        insrToFill, insrToFillFP = self.execution_r
        
        if insrToFill != 0:
            self.ALU.addInstruction(insrToFill)
            
        if insrToFillFP != 0:
            self.FPA.addInstruction(insrToFillFP)
        else:
            self.FPA.addInstruction(None)
        self.FPA.updateHistory()
        self.activeList.updateHistory()
        
    def commit_calc(self):
        print 'commiting'
        for i in range(min(4, self.activeList.getLength())):
            insr = self.activeList.graduateInstruction()
            if insr != 0:
                insr.addHistory('C')
                print insr.getHistory()
                print 'commiting instruction', insr.getTag()
                args = insr.getArgs()
                destination_arg = args[0]
                # reset that argument to 0
                destination_arg.setBusyBit(0)
                # free the old mapping
                mapInfo = insr.getRegMapInfo()
                old_reg = mapInfo[1]
                self.freeList.addReg(old_reg)
    
    def updateHistoryInIntegerQueue(self):
        for i in range(self.integerQueue.getLength()):
            insr = self.integerQueue.getElem(i)
            insr.addHistory(' ')
            
    def updateHistoryInFPQueue(self):
        for i in range(self.FPqueue.getLength()):
            insr = self.FPqueue.getElem(i)
            insr.addHistory(' ')
    
    def oneClock(self):
        
        # The calc part
        self.fetch_calc()
        self.decode_calc()
        self.issue_calc()
        self.execution_calc()
        self.commit_calc()
        
        # the edge part
        self.updateHistoryInInsrSet()
        self.updateHistoryInIntegerQueue()
        self.updateHistoryInFPQueue()
        
        self.fetch_edge()
        self.decode_edge()
        self.issue_edge()
        self.execution_edge()
        
        
        
    
    
        
        
        
        
        
        