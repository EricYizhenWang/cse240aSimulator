from collections import deque
class ALU:
    def __init__(self):
        self.queue = deque()
    
    def addInstruction(self, insr):
        self.queue.append(insr)
        
    def popInstruction(self):
        if len(self.queue) != 0:
            insr = self.queue.popleft()
            return insr
        else:
            return 0
    # This is very complicated...
    # For integer registers
    # TODO: set the busybit of that old register to 0
    # and then pop from the system