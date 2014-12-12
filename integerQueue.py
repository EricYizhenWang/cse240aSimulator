from collections import deque

class integerQueue:
    def __init__(self):
        self.queue = deque()
        self.maxSize = 16
    
    # This part involves combinatorial logic and should have been done outside
    # the object!
    def resolveOperand(self, insr):
        # This function resolves the instruction operand from logical register
        # to physical register
        return 0
        
    def addInstruction(self, insr):
        self.queue.append(insr)
        
    def popInstruction(self, index):
        self.queue.rotate(index)
        self.queue.pop()
        self.queue.rotate(-1*index)
    
    # This is also combinatoric logic that should be done outside the object!    
    def searchExecutableInsr(self):
        # This function searches all instructions that are ready to execute
        # Here basically it means its operands are ready
        insr_list = []
        for i in range(len(self.queue)):
            insr = self.queue[i]
            args = insr.getArgs()
            #if args[1].
            