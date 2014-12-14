from collections import deque
class activeList:
    def __init__(self):
        # The activelist queue contains instruction objects that are 
        # active in the processor
        
        # The mapping queue contains the mapping between logical destination
        # register and the old corresponding physical register.
        
        self.queue = deque()
        #self.mappingQueue = deque()
        self.length = len(self.queue)
        self.maxSize = 32
        
    def getLength(self):
        return self.length
    def getContent(self):
        return self.queue
    
    def addInstruction(self, insr):
        self.queue.append(insr)
        #self.mappingQueue.append(mapping)
        #self.length = self.length + 1
        
    def graduateInstruction(self):
        if len(self.queue) > 0:
            insr = self.queue[0]
            if insr.getDoneBit() == 1:
                self.queue.popleft()
            #self.mappingQueue.popleft()
            #self.length = self.length - 1
    
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
        
        #tag = insr.getTag()
        #for i in range(len(self.queue)):
        #    insrToCompare = self.queue[i]
        #    tagToCompare = insrToCompare.getTag()
        #    if tagToCompare == tag:
        #        insrToCompare.setDoneBit(1)
        destinationInsr = self.searchInstruction(insr)
        destinationInsr.setDoneBit(1)
    
    
        
    
    
    