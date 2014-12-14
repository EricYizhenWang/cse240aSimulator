from collections import deque

class instruction:
    def __init__(self, typeOfInsr, args, tag):
        # An instruction has:
        #   -- Type: B, A, M, I, S/L
        #   -- Args: a list of arguments 
        #   -- Tag: a unique digit ID 
        #   -- DoneBit: whether it has been poped out of the instruction queue
        #               and executed
        self.t = typeOfInsr
        self.args = args
        self.tag = tag
        self.doneBit = 0
        # This regMapEntry stores the old logical-physical register mapping.
        self.regMapEntry = []
        # This entry stores the execution history of the instruction
        self.history = []
        
    def getHistory(self):
        return self.history
    
    def addHistory(self, act):
        self.history.append(act)
        
    def getRegMapInfo(self):
        return self.regMapEntry
    def setRegMapInfo(self, mapEntry):
        self.regMapEntry = mapEntry
        
    def getType(self):
        return self.t
    
    def setDoneBit(self, doneBit):
        self.doneBit = doneBit
        
    def getDoneBit(self):
        return self.doneBit
    
    def getTag(self):
        return self.tag
    
    def getArgs(self):
        return self.args
    
    def setArgs(self, args):
        self.args = args
        
    def setArgs_i(self, arg, i):
        self.args[i] = arg
        
class register:
    def __init__(self, typeR, tag):
        # The register has a type field to indicate if it's logical or physical.
        # It also has a unique (type, digit ID) couple to identify.
        self.t = typeR
        self.tag = tag
        self.busyBit = 0
        
    def getType(self):
        return self.t
    def getTag(self):
        return self.tag
    def getID(self):
        return [self.t, self.tag]
    def getBusyBit(self):
        return self.busyBit
    def setBusyBit(self, value):
        self.busyBit = value
        

class regMapTable:
    def __init__(self):
        self.maxSize = 32
        self.table = [0] * self.maxSize
    
    def getMapping(self, regLogicalIndex):
        return self.table[regLogicalIndex]
    
    def setMapping(self, regLogicalIndex, physicalReg):
        self.table[regLogicalIndex] = physicalReg
        
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


class FPqueue:
    def __init__(self):
        self.queue = deque()
        self.maxSize = 16
    
    def getLength(self):
        return len(self.queue)
    
    def getElem(self, index):
        return self.queue[index]
        
    def addInstruction(self, insr):
        self.queue.append(insr)
        
    def addInsrSet(self, insrSet):
        for i in range(len(insrSet)):
            insr = insrSet.popleft()
            self.queue.append(insr)
        
    def popInstruction(self, index):
        self.queue.rotate(-1*index)
        insr = self.queue.popleft()
        self.queue.rotate(index)
        return insr
        
    def searchExecutableInsr(self, t):
        # This function searches all instructions that are ready to execute
        # Here basically it means its operands are ready
        
        insr_list = []
        for i in range(len(self.queue)):
            insr = self.queue[i]
            args = insr.getArgs()
            type_insr = insr.getType()
            
            if type_insr == t:
                flag = 1
                for j in range(1,len(args)):
                    if args[j] == 0:
                        pass
                    elif args[j].getBusyBit() == 1:
                        flag = 0
                if flag == 1:
                    insr_list.append([self.queue[i], i])
        return insr_list
        
    def sendInsrForExecution(self, t):
        l = self.searchExecutableInsr(t)
        if len(l) > 0:
            toPop = l[0]
            return self.popInstruction(toPop[1])
        else:
            return 0
        
class FPunit:
    def __init__(self, t):
        self.queue = deque([None, None, None])
        self.finishTime = 0
        self.inUse = 0
        self.t = t
        
    def ifInUse(self):
        return self.inUse
    
    #def getFinishTime(self):
    #    return self.finishTime
    
    def addInstruction(self, insr):
        self.queue.append(insr)
        #self.queue.finishTime = self.timeNeeded
        
    def reduceFinishTime(self):
        self.queue.finishTime = self.queue.finishTime - 1
        
    def popInstruction(self):
        if len(self.queue) != 0:
            insr = self.queue.popleft()
            if insr == None:
                return None
            else:
                arg = insr.getArgs()
                destination_arg = arg[0]
                destination_arg.setBusyBit(0)
                return insr
        else:
            return 0    
    
    def updateHistory(self):
        for i in range(len(self.queue)):
            insr = self.queue[i]
            if insr != None:
                insr.addHistory(self.t)
                
class insrBuffer:
    # This object stores the fetched instructions that are ready for decoding.
    def __init__(self):
        self.queue = deque()
        
    def getLength(self):
        return len(self.queue)
    
    def addInstruction(self, insr):
        self.queue.append(insr)
        
    def addInsrSet(self, insrSet):
        for i in range(len(insrSet)):
            self.queue.append(insrSet[i])
            
    def popInstruction(self):
        return self.queue.popleft()

class integerQueue:
    def __init__(self):
        self.queue = deque()
        self.maxSize = 16
    
    def getLength(self):
        return len(self.queue)
    
    def getElem(self, index):
        return self.queue[index]
        
    def addInstruction(self, insr):
        self.queue.append(insr)
        
    def addInsrSet(self, insrSet):
        for i in range(len(insrSet)):
            insr = insrSet.popleft()
            self.queue.append(insr)
        
    def popInstruction(self, index):
        self.queue.rotate(-1*index)
        insr = self.queue.popleft()
        self.queue.rotate(index)
        return insr
    
    # This is also combinatoric logic that should be done outside the object!    
    def searchExecutableInsr(self):
        # This function searches all instructions that are ready to execute
        # Here basically it means its operands are ready
        
        insr_list = []
        for i in range(len(self.queue)):
            insr = self.queue[i]
            args = insr.getArgs()
            
            flag = 1
            for j in range(1,len(args)):
                #print args[j]
                if args[j] == 0:
                    pass
                elif args[j].getBusyBit() == 1:
                    flag = 0
            if flag == 1:
                insr_list.append([self.queue[i], i])
        return insr_list
        
    def sendInsrForExecution(self):
        l = self.searchExecutableInsr()
        if len(l) > 0:
            toPop = l[0]
            #print toPop, 'toPop'
            return self.popInstruction(toPop[1])
        else:
            return 0
            
class ALU:
    def __init__(self):
        self.queue = deque()
        
    def getLength(self):
        return len(self.queue)
    
    def addInstruction(self, insr):
        self.queue.append(insr)
        
    def popInstruction(self):
        if len(self.queue) != 0:
            insr = self.queue.popleft()
            arg = insr.getArgs()
            destination_arg = arg[0]
            destination_arg.setBusyBit(0)
            return insr
        else:
            return 0
    # This is very complicated...
    # For integer registers
    # TODO: set the busybit of that old register to 0
    # and then pop from the system
    
class activeList:
    def __init__(self):
        # The activelist queue contains instruction objects that are 
        # active in the processor
        
        # The mapping queue contains the mapping between logical destination
        # register and the old corresponding physical register.
        
        self.queue = deque()
        self.length = len(self.queue)
        self.maxSize = 32
        
    def getLength(self):
        return len(self.queue)
    def getContent(self):
        return self.queue
    
    def addInstruction(self, insr):
        self.queue.append(insr)
        
    def addInsrSet(self, insrSet):
        for i in range(len(insrSet)):
            self.queue.append(insrSet[i])
        
    def graduateInstruction(self):
        if len(self.queue) > 0:
            insr = self.queue[0]
            if insr.getDoneBit() == 1:
                return self.queue.popleft()
            else:
                return 0
    
    def searchInstruction(self, insr):
        tag = insr.getTag()
        for i in range(len(self.queue)):
            insrToCompare = self.queue[i]
            tagToCompare = insrToCompare.getTag()
            if tagToCompare == tag:
                return insrToCompare
    
    def setInsrDoneBit(self, insr):
        # when the instruction is poped out of the instruction queues, 
        # compare the tag to identify the instruction in the active list 
        # and make it done.
        destinationInsr = self.searchInstruction(insr)
        print 'destination', destinationInsr
        destinationInsr.setDoneBit(1)
        print (destinationInsr == self.queue[0]), 'flag check'
        print destinationInsr.getTag(), self.queue[0].getTag()
    
    def updateHistory(self):
        for i in range(len(self.queue)):
            if self.queue[i].getDoneBit() == 1:
                self.queue[i].addHistory(' ')
                

