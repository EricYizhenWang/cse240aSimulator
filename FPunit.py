from collections import deque

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