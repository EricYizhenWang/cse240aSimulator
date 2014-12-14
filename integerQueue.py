from collections import deque

class integerQueue:
    def __init__(self):
        self.queue = deque()
        self.maxSize = 16
    
    # This part involves combinatorial logic and should have been done outside
    # the object!
    def resolveOperand(self, insr, regMap):
        # This function resolves the instruction operand from logical register
        # to physical register
        
        # the case for integer value
        
        #args_phy.append(regMap.getMapping(args[1]))
        #args_phy.append(regMap.getMapping(args[2]))
        return 0
        
        
    def addInstruction(self, insr):
        self.queue.append(insr)
        
    def popInstruction(self, index):
        self.queue.rotate(index)
        insr = self.queue.pop()
        self.queue.rotate(-1*index)
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
                print args[j]
                if args[j] == 0:
                    pass
                elif args[j].getBusyBit() == 1:
                    flag = 0
            if flag == 1:
                insr_list.append([self.queue[i], i])
        return insr_list
        #if args[1].
        
    def sendInsrForExecution(self):
        l = self.searchExecutableInsr()
        if len(l) > 0:
            toPop = l[0]
            return popInstruction(toPop[1])
            