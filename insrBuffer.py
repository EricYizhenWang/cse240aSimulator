from collections import deque
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