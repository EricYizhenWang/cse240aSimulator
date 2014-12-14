from collections import deque
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
    
    
        
    
    
    