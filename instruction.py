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