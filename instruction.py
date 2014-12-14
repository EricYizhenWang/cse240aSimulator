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