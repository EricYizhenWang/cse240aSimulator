from collections import deque
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
