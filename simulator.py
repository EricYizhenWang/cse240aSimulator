from collections import deque
from basicComponents import activeList, freeList, integerQueue, \
     regMapTable, register, instruction, ALU, insrBuffer, FPunit, FPqueue, addressQueue, SLunit

from copy import deepcopy

class simulator:
    def __init__(self):
        self.activeList = activeList()
        self.freeList = freeList()
        self.integerQueue = integerQueue()
        self.FPqueue = FPqueue()
        self.addrQueue = addressQueue()
        self.regMapTable = regMapTable()
        self.ALU = ALU()
        self.FPA = FPunit('A')
        self.FPM = FPunit('M')
        self.SLunit = SLunit()
        self.initializeRegMap()
        self.insrSet = deque()
        self.fetchedList = insrBuffer()
        self.decodedList = insrBuffer()
        
        # Set the machine parameters including queue size etc.
        self.maxIntQ = 16
        self.maxFPQ = 16
        self.maxAddrQ = 16
        self.maxActiveList = 32
        self.maxPhysReg = 64
        
        self.fetch_r = deque()
        self.decode_r = deque()
        self.issue_r = []
        self.execution_r = []
        self.ls_r = None
        
        self.toSetDoneBit = []
     
    def setInsrSet(self, insrSet):
        self.insrSet = insrSet
    
    def getElemFromInsrSet(self):
        if len(self.insrSet)>0:
            #print len(self.insrSet)
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
            #print new_value.getTag()
            self.regMapTable.setMapping(regLogicalIndex, new_value)
            self.freeList.setBusyBit(new_value.getTag(), 1)
            return [regLogicalIndex, old_value, new_value]
        
    def resolveOperand_I_A_M(self, insr):
        args = insr.getArgs()
        #resolveTheOperand
        #print 'This is executed', args
        for i in range(1,3):
            new_arg = self.regMapTable.getMapping(args[i])
            #print i, new_arg.getTag()
            insr.setArgs_i(new_arg, i)
        #resolveTheDestination
        newMapInfo = self.assignNewMapping(args[0])
        insr.setRegMapInfo(newMapInfo[0:2])
        insr.setArgs_i(newMapInfo[2],0)
        
    def resolveOperand_L(self, insr):
        args = insr.getArgs()
        destination = args[0]
        source = args[1]
        
        # resolve the source
        new_source = self.regMapTable.getMapping(source)
        insr.setArgs_i(new_source, 1)
        
        # assign the destination physical register
        newMapInfo = self.assignNewMapping(destination)
        insr.setRegMapInfo(newMapInfo[0:2])
        insr.setArgs_i(newMapInfo[2],0)
        
        # leave the address field as it is
        
    def resolveOperand_S(self, insr):
        args = insr.getArgs()
        for i in range(2):
            arg = args[i]
            new_arg = self.regMapTable.getMapping(arg)
            insr.setArgs_i(new_arg, i)
            
        # leave the address field as it is
        
    def resolveOperand(self, insr):
        # This function resolves the insr's arguments into physical registers
        #args = insr.getArgs()
        type_insr = insr.getType()
        numSpareReg = self.freeList.numSpareReg()
        if (type_insr == 'I') or (type_insr == 'A') or (type_insr == 'M'):
            if numSpareReg > 0:
                self.resolveOperand_I_A_M(insr)
                return 0
            else:
                return insr
        elif (type_insr == 'S'):
            self.resolveOperand_S(insr)
            return 0
        elif (type_insr == 'L'):
            if numSpareReg > 0:
                self.resolveOperand_L(insr)
                return 0
            else:
                return insr
        
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
        #print 'decoding'
        decode_q = deque()
        recycle_q = deque()
        l = min(4, self.fetchedList.getLength())
        for i in range(l):
            insr = self.fetchedList.popInstruction()
            #Assume Integer operation now
            result = self.resolveOperand(insr)
            # decode successful if result == 0
            if result == 0:
                insr.addHistory('D')
                decode_q.append(insr)
            else:
                recycle_q.append(insr)
        
        # push the recycle_queue back
        for i in range(len(recycle_q)):
            insr = recycle_q.pop()
            self.fetchedList.addBackInstruction(insr)
        
        for i in range(self.fetchedList.getLength()):
            insr = self.fetchedList.getElem(i)
            insr.addHistory(' ')
            
        self.decode_r = decode_q
    
    def decode_edge(self):
        decode_q = self.decode_r
        self.decodedList.addInsrSet(decode_q)

    def issue_calc(self):
        #print 'issuing'
        recycle_queue = deque()
        
        l = min(4, self.decodedList.getLength())
        toActiveList = deque()
        activeListSpare = self.activeList.numSpare()
        
        toIntegerQueue = deque()
        intQueueSpare = self.integerQueue.numSpare()
        
        toFPqueue = deque()
        FPQueueSpare = self.FPqueue.numSpare()
        print FPQueueSpare, 'num of free FP queue'
        
        toAddrQueue = deque()
        addrQueueSpare = self.addrQueue.numSpare()
        for i in range(l):
            insr = self.decodedList.popInstruction()
            insr_type = insr.getType()
            
            if activeListSpare > 0:
                #TODO: add different type of insr here
                if insr_type == 'I':
                    if intQueueSpare > 0:
                        toIntegerQueue.append(insr)
                        toActiveList.append(insr)
                        intQueueSpare = intQueueSpare - 1
                        activeListSpare = activeListSpare - 1
                        insr.addHistory('I')
                    else:
                        recycle_queue.append(insr)
                elif (insr_type == 'A') or (insr_type == 'M'):
                    print FPQueueSpare, 'num of free FP queue'
                    if FPQueueSpare > 0:
                        toFPqueue.append(insr)
                        toActiveList.append(insr)
                        FPQueueSpare = FPQueueSpare - 1
                        activeListSpare = activeListSpare - 1
                        insr.addHistory('I')
                    else:
                        recycle_queue.append(insr)
                elif (insr_type == 'S') or (insr_type == 'L'):
                    if addrQueueSpare > 0:
                        toAddrQueue.append(insr)
                        toActiveList.append(insr)
                        addrQueueSpare = addrQueueSpare - 1
                        activeListSpare = activeListSpare -1
                        insr.addHistory('I')
                    else: 
                        recycle_queue.append(insr)
        # push that recycle_queue entry back. It's actually a stack!
        l = len(recycle_queue)
        for i in range(l):
            insr = recycle_queue.pop()
            self.decodedList.addBackInstruction(insr)
            #insr.addHistory(' ')
        l = self.decodedList.getLength()
        for i in range(l):
            insr = self.decodedList.getElem(i)
            insr.addHistory(' ')
                
        print 'numFPadded', len(toFPqueue)
        self.issue_r = [toActiveList, toIntegerQueue, toFPqueue, toAddrQueue]
    
    def issue_edge(self):
        toActiveList, toIntegerQueue, toFPqueue, toAddrQueue = self.issue_r
        self.activeList.addInsrSet(toActiveList)
        self.integerQueue.addInsrSet(toIntegerQueue)
        self.FPqueue.addInsrSet(toFPqueue)
        self.addrQueue.addInsrSet(toAddrQueue)
    
    def ALU_calc(self):
        popedInsr = self.integerQueue.sendInsrForExecution()
        if popedInsr != 0:
            self.ALU.addInstruction(popedInsr)
        #print 'ALUqueue length', self.ALU.getLength()
        insr = self.ALU.popInstruction()
        #print 'insr=', insr
        if insr != 0:
            tag = insr.getTag()
            #self.activeList.setInsrDoneBit(insr)
            self.toSetDoneBit.append(insr)
            insr.addHistory('E')
            
            # Set busybits to zeros
            args = insr.getArgs()
            args[0].setBusyBit(0)
            
    def FPA_calc(self):
        #
        
        popedFPInsr1 = self.FPqueue.sendInsrForExecution('A')
        if popedFPInsr1 != 0:
            self.FPA.addInstruction(popedFPInsr1)
        else:
            self.FPA.addInstruction(None)
        self.FPA.updateHistory() 
        #FPA.addInstruction()
        insr = self.FPA.popInstruction()
        #print insr
        if insr == None:
            pass
        else: 
            tag = insr.getTag()
            #self.activeList.setInsrDoneBit(insr)
            self.toSetDoneBit.append(insr)
        #print self.toSetDoneBit
            
    def FPM_calc(self):
        #
        popedFPInsr1 = self.FPqueue.sendInsrForExecution('M')
        if popedFPInsr1 != 0:
            self.FPM.addInstruction(popedFPInsr1)
        else:
            self.FPM.addInstruction(None)
        self.FPM.updateHistory()
        insr = self.FPM.popInstruction()
        #print insr
        if insr == None:
            pass
        else: 
            tag = insr.getTag()
            #self.activeList.setInsrDoneBit(insr)
            self.toSetDoneBit.append(insr)
            
    def SLunit_calc(self):
        insr = self.SLunit.popInstruction()
        #print 'insr', insr == None, insr.getTag()
        if insr != None:
            #print insr.getTag()
            #print 'Done bit before', insr.getDoneBit()
            #print '???'
            #print 'insr == None?', insr == None
            insr_type = insr.getType()
            #self.activeList.setInsrDoneBit(insr)
            #print 'Done bit now', insr.getDoneBit()
            self.toSetDoneBit.append(insr)
            insr.addHistory(insr_type)
            
    def SLunit_edge(self):
        if self.ls_r != None:
            #print 'SLunit_edge_to_add', self.ls_r.getTag()
            if self.ls_r.getDoneBit() != 1:
                self.SLunit.addInstruction(self.ls_r)
                
    def SL_add_unit_edge(self):
        #if self.ls_r != None:
        #    print self.ls_r.getTag(), 'this is self.ls_r'
        #    print self.ls_r.getDoneBit(), 'this is the Done Bit'
            #self.activeList.setInsrDoneBit(self.ls_r)
            #self.SLunit.addInstruction(self.ls_r)
            #self.ls_r = None
            #print 'self.ls_r is empty', None == self.ls_r
        self.addrQueue.updateHistory()        
        self.addrQueue.sendForAddressCalc_edge()
        
        # Load the possible choices of instructions from addrQueue
        insrSet = self.addrQueue.sendForExecution()
        #print len(insrSet), 'numOfInstructionsToChooseFrom'
        # Find the first store option
        l = len(insrSet)
        first_store_position = -1
        first_store = None
        for i in range(l):
            insr = insrSet[i]
            if insr.getDoneBit() != 1:
                insr_type = insr.getType()
                if insr_type == 'S':
                    first_store = insr
                    first_store_position = i
                    break
                
        # Find the first load option
        first_load_position = -1
        first_load = None
        for i in range(l):
            insr = insrSet[i]
            insr_type = insr.getType()
            if insr.getDoneBit() != 1:
                if insr_type == 'L':
                    first_load = insr
                    first_load_position = i
                    break
            
        # If the first option is load, execute it
        if first_load_position == 0:
            tag = first_load.getTag()
            self.ls_r = first_load
            #self.activeList.setInsrDoneBit(first_load)
            # reset the destination busy bit
            args = first_load.getArgs()
            args[0].setBusyBit(0)
        # else, if the first option is store
        elif first_store_position == 0:
            # if it is at the head of activeList, go
            activeListHead = self.activeList.getElem(0)
            if first_store.getTag() == activeListHead.getTag():
                self.ls_r = first_store
                #self.activeList.setInsrDoneBit(first_store)
                # else, execute the first load option, if any
            else:
                if (first_load != 0) and (first_load != None):
                    self.ls_r = first_load
                    #self.activeList.setInsrDoneBit(first_load)
                    args = first_load.getArgs()
                    args[0].setBusyBit(0)
        
        if self.ls_r != None:        
            if self.ls_r.getType == 'L':
                args = self.ls_r.getArgs()
                args[0].setBusyBit(0)
        #print self.ls_r, 'this is self.ls_r'
        # TODO: check if it belons to here            
        

        
    def SL_add_unit_calc(self):
        # addressCalculation
        self.addrQueue.sendForAddressCalc_calc()
        
        ## Load the possible choices of instructions from addrQueue
        #insrSet = self.addrQueue.sendForExecution()
        #print len(insrSet), 'numOfInstructionsToChooseFrom'
        ## Find the first store option
        #l = len(insrSet)
        #first_store_position = -1
        #first_store = None
        #for i in range(l):
            #insr = insrSet[i]
            #if insr.getDoneBit() != 1:
                #insr_type = insr.getType()
                #if insr_type == 'S':
                    #first_store = insr
                    #first_store_position = i
                    #break
                
        ## Find the first load option
        #first_load_position = -1
        #first_load = None
        #for i in range(l):
            #insr = insrSet[i]
            #insr_type = insr.getType()
            #if insr.getDoneBit() != 1:
                #if insr_type == 'L':
                    #first_load = insr
                    #first_load_position = i
                    #break
            
        ## If the first option is load, execute it
        #if first_load_position == 0:
            #tag = first_load.getTag()
            #self.ls_r = first_load
            ##self.activeList.setInsrDoneBit(first_load)
            ## reset the destination busy bit
            #args = first_load.getArgs()
            #args[0].setBusyBit(0)
        ## else, if the first option is store
        #elif first_store_position == 0:
            ## if it is at the head of activeList, go
            #activeListHead = self.activeList.getElem(0)
            #if first_store.getTag() == activeListHead.getTag():
                #self.ls_r = first_store
                ##self.activeList.setInsrDoneBit(first_store)
                ## else, execute the first load option, if any
            #else:
                #if (first_load != 0) and (first_load != None):
                    #self.ls_r = first_load
                    ##self.activeList.setInsrDoneBit(first_load)
                    #args = first_load.getArgs()
                    #args[0].setBusyBit(0)    
        ## TODO: check if it belons to here            
        
        
    def execution_calc(self):
        #print 'execution'
        self.ALU_calc()
        self.FPA_calc()   
        self.FPM_calc()
        self.SL_add_unit_calc()
        self.SLunit_calc()
        # get the refill units to ALU ready
        #popedInsr = self.integerQueue.sendInsrForExecution()
        #popedFPInsr1 = self.FPqueue.sendInsrForExecution('A')
        #popedFPInsr2 = self.FPqueue.sendInsrForExecution('M')
        #self.execution_r = [popedFPInsr1, popedFPInsr2]
        
    def execution_edge(self):
        # Then fill the pipeline with the next instruction
        #if (len(self.integerQueue.queue)>0) and (self.ALU.getLength() == 0):
        #insrToFill, 
        #insrToFillFPA, insrToFillFPM = self.execution_r
        
        #if insrToFill != 0:
        #    self.ALU.addInstruction(insrToFill)
            
        #if insrToFillFPA != 0:
        #    self.FPA.addInstruction(insrToFillFPA)
        #else:
        #    self.FPA.addInstruction(None)
            
        #if insrToFillFPM != 0:
        #    self.FPM.addInstruction(insrToFillFPM)
        #else:
        #    self.FPM.addInstruction(None)
        #return 0    
        
        self.SL_add_unit_edge()
        self.SLunit_edge()
        #self.FPA.updateHistory()
        #self.FPM.updateHistory()
        #self.activeList.updateHistory()
        
    def commit_edge(self):
        self.activeList.updateHistory()
        lst = self.toSetDoneBit
        l = len(lst)
        for i in range(l):
            insr = lst[i]
            #print insr.getTag()
            self.activeList.setInsrDoneBit(insr)
        self.toSetDoneBit = []
            
    def commit_calc(self):
        #print 'commiting'
        for i in range(min(4, self.activeList.getLength())):
            insr = self.activeList.graduateInstruction()
            if insr != 0:
                
                insr_type = insr.getType()

                
                if (insr_type == 'A') or (insr_type == 'I') or (insr_type == 'M'):
                    args = insr.getArgs()
                    destination_arg = args[0]
                    # reset that argument to 0
                    destination_arg.setBusyBit(0)
                    # free the old mapping
                    mapInfo = insr.getRegMapInfo()
                    old_reg = mapInfo[1]
                    self.freeList.addReg(old_reg)
                elif (insr_type == 'S'):
                    # pop that instruction from addrQueue
                    self.addrQueue.popInstruction()
                    #insr.popHistory()
                    #insr.addHistory('S')
                    pass
                elif (insr_type == 'L'):
                    # free the old register
                    mapInfo = insr.getRegMapInfo()
                    #print mapInfo, 'this is mapInfo'
                    old_reg = mapInfo[1]
                    self.freeList.addReg(old_reg)
                    # pop that instruction from addrQueue
                    self.addrQueue.popInstruction()
                    #insr.popHistory()
                    #insr.addHistory('L')
                    
                insr.addHistory('C')
                print len(insr.getHistory()), insr.getHistory()
                print 'commiting instruction', insr.getTag()
                
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
        
        
        
        
                
        
        
        self.commit_edge()
        self.execution_edge()
        self.issue_edge()
        self.decode_edge()
        self.fetch_edge()
        
    
    
        
        
        
        
        
        